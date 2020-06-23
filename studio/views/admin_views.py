from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, ListView
from sweetify import sweetify
from django.shortcuts import redirect

from alumnica_model.mixins import  OnlyAdministratorMixin
from alumnica_model.models import  AuthUser
from studio.forms.user_forms import  CreateUserForm, UpdateUserForm

from django.views import View
from alumnica_model.models.users import TYPE_ADMINISTRATOR, TYPE_CONTENT_CREATOR, TYPE_SUPERVISOR



from django.conf import settings
from django.forms.models import model_to_dict
from alumnica_model.models import Ambit, Subject, ODA, Tag, Moment
from alumnica_model.models import content 

import requests


class SyncDB(LoginRequiredMixin,  OnlyAdministratorMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            ambits_pub = Ambit.objects.filter(is_published=True)            
            for ambit in ambits_pub:
                name_ambit = ambit.name
                subject_pub = ambit.subjects.all()
                for  subject in subject_pub:
                    name_subject = subject.name
                    odas_pub = subject.odas.all()
                    for oda in odas_pub:
                        name_oda = oda.name
                        oda.is_published=True
                        oda.save()
                        oda_map = model_to_dict(oda, fields = ODA_DATA)
                        oda_map['subject'] = name_subject
                        oda_map['ambit'] = name_ambit
                        oda_map['tags'] = list (map (lambda x: x.name, oda.tags.all()))
                        oda_map['timestamp'] = firestore.SERVER_TIMESTAMP
                        oda_map['active_icon'] = str (oda.active_icon.file.url).replace(WS_S3, '')
                        content_data = requests.get(str (oda.active_icon.file.url)).content
                        blob = settings.bucket.blob(str (oda.active_icon.file.url).replace(WS_S3, ''))
                        oda_map['completed_icon'] = str (oda.completed_icon.file.url).replace(WS_S3, '')
                        content_data = requests.get(str (oda.completed_icon.file.url)).content
                        blob = settings.bucket.blob(str (oda.completed_icon.file.url).replace(WS_S3, ''))
                                                
                        oda_ref = settings.db.collection(u'odas').document(name_oda)
                        oda_ref.set(oda_map)
                        microodas_pub = oda.microodas.all()
                        for microoda in microodas_pub:
                            name_microoda = microoda.name
                            moments_pub = microoda.activities.all()
                            for moment in moments_pub:
                                name_moment = moment.name
                                moment.is_published=True
                                moment.save()
                                moment_map = model_to_dict(moment, fields = MOMENTS_DATA)
                                moment_map['oda'] = name_oda
                                moment_map['microooda'] = name_microoda
                                moment_map['tags'] = list (map (lambda x: x.name, moment.tags.all()))
                                moment_map['timestamp'] = settings.firestore.SERVER_TIMESTAMP
                                print (moment_map)
                                if moment.type in ['mp4','img']:
                                    content_data = requests.get(str (moment.content)).content
                                    blob = settings.bucket.blob(str (moment.content).replace (WS_S3,''))
                                    if moment.type == 'mp4':
                                        content_type_data = 'video/mp4'
                                    else:
                                        content_type_data = 'image/jpg'                                
                                    blob.upload_from_string(
                                            content_data,
                                            content_type=content_type_data
                                        )                                
                                    moment_map['url'] =  blob.public_url
                                else:
                                    moment_map['url'] = str (moment.content)
                                moment_ref = settings.db.collection(u'moments').document(name_moment)
                                moment_ref.set(moment_map)
            sweetify.success(self.request, 'BD Syncronized', persistent='Ok')
        except Exception:
            sweetify.error(self.request, 'BD Not Syncronized', persistent='Ok')
        return redirect(to="dashboard_view")
    



class UsersView(LoginRequiredMixin, OnlyAdministratorMixin, ListView):
    """
    Users dashboard view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/users.html'
    queryset = AuthUser.objects.filter(Q(user_type=TYPE_SUPERVISOR) | Q(user_type=TYPE_CONTENT_CREATOR) | Q(user_type=TYPE_ADMINISTRATOR))
    context_object_name = 'users_list'


class CreateUserView(LoginRequiredMixin, OnlyAdministratorMixin, CreateView):
    """
    Create new AuthUser object view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/users-edit.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('dashboard_view')

    def form_invalid(self, form):
        sweetify.error(self.request, form.errors['email'][0], persistent='Ok')
        context = self.get_context_data()
        return self.render_to_response(context)

    def form_valid(self, form):
        user = form.save()
        sweetify.success(self.request, "Usuario creado", persistent='Ok')
        return super(CreateUserView, self).form_valid(form)


class UpdateUserView(LoginRequiredMixin, OnlyAdministratorMixin, UpdateView):
    """
    Update existing user view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/users-edit.html'
    form_class = UpdateUserForm
    success_url = reverse_lazy('dashboard_view')

    def get_object(self, queryset=None):
        return AuthUser.objects.get(pk=self.kwargs['pk'])

    def form_invalid(self, form):
        sweetify.error(self.request, form.errors['email'][0], persistent='Ok')
        context = self.get_context_data()
        return self.render_to_response(context)

    def form_valid(self, form):
        user = form.save()
        sweetify.success(self.request, "Información de usuario actualizada", persistent='Ok')
        return super(UpdateUserView, self).form_valid(form)
