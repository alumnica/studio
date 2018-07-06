from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, FormView

from alumnica_model.models import Ambit, users, Subject, ODA


class ApproveToPublishDashboard(LoginRequiredMixin, FormView):
    login_url = "login_view"
    template_name = "studio/dashboard/supervisor.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != users.TYPE_SUPERVISOR:
            return redirect(to="dashboard_view")
        else:
            return super(ApproveToPublishDashboard, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        ambits = Ambit.objects.filter(is_draft=False, is_published=False)
        ambits_list = []
        for ambit in ambits:
            odas = [len(subject.odas.all()) for subject in ambit.subjects.all()]
            moments = []
            for subject in ambit.subjects.all():
                for oda in subject.odas.all():
                    moments = [len(microoda.activities.all()) for microoda in oda.microodas.all()]

            ambits_list.append([ambit, sum(odas), sum(moments)])
        return {'ambits_list': ambits_list}


class AmbitPreviewView(LoginRequiredMixin, FormView):
    login_url = "login_view"
    template_name = "studio/dashboard/supervisor-vp-ambito.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != users.TYPE_SUPERVISOR:
            return redirect(to="dashboard_view")
        else:
            return super(AmbitPreviewView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        ambit = Ambit.objects.get(pk=self.kwargs['pk'])
        context.update({'ambit': ambit})
        return context


class GridPositionView(LoginRequiredMixin, FormView):
    login_url = "login_view"
    template_name = ""

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != users.TYPE_SUPERVISOR:
            return redirect(to="dashboard_view")
        else:
            return super(GridPositionView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GridPositionView, self).get_context_data(**kwargs)
        ambits_list = Ambit.objects.filter(is_published=True).order_by('position')
        ambit = Ambit.objects.get(pk=self.kwargs['pk'])
        context.update({'ambits_list': ambits_list, 'new_ambit': ambit})

    def form_valid(self, form):
        position_array = self.request.POST.get('positions').split(';')
        for element in position_array:
            ambit_position = element.split(',')
            ambit = Ambit.objects.get(pk=ambit_position[0])
            ambit.position = ambit_position[1]
            ambit.save()
        return redirect(to="")


class ODAsPositionSubjectPreview(LoginRequiredMixin, FormView):
    login_url = "login_view"
    template_name = "studio/dashboard/supervisor-vp-materia.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != users.TYPE_SUPERVISOR:
            return redirect(to="dashboard_view")
        else:
            return super(ODAsPositionSubjectPreview, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        subject = Subject.objects.get(pk=self.kwargs['pk'])
        section_images_list = subject.sections_images.all()
        odas_list = []
        section_counter = 1
        for section in subject.sections_images.all():
            odas_list.append(subject.odas.all().filter(section=section_counter))
            section_counter += 1

        zones = ['a', 'b', 'c', 'd']
        subject_zip = zip(section_images_list, zones)
        context.update({'subject_zip': subject_zip, 'odas_list': odas_list})
        return context


class MicroodaPreview(LoginRequiredMixin, FormView):
    login_url = "login_view"
    template_name = ""

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != users.TYPE_SUPERVISOR:
            return redirect(to="dashboard_view")
        else:
            return super(MicroodaPreview, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MicroodaPreview, self).get_context_data(**kwargs)
        microodas = ODA.objects.get(pk=self.kwargs['pk']).microodas.all()
        context.update({'microodas': microodas})
        return context