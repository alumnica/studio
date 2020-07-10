from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from alumnica_model.mixins import OnlyContentCreatorAndSupervisorMixin

from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from studio.services.moment import get_context_data, get_context_data_update, form_valid
from alumnica_model.models import Moment
from studio.forms.moment_forms import MomentCreateForm, MomentUpdateForm, ContentForm
from alumnica_model.models.content import Content


class MomentsView(LoginRequiredMixin, OnlyContentCreatorAndSupervisorMixin, ListView):
    """
    Momentos dashboard view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/momentos.html'
    queryset = Moment.objects.all()
    context_object_name = 'moments_list'


class CreateMomentView(LoginRequiredMixin, CreateView):
    """
    Create new Momento object view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/momentos-edit.html'
    form_class = MomentCreateForm

    
    def get_context_data(self, **kwargs):
        context = super(CreateMomentView, self).get_context_data(**kwargs)
        get_context_data(context,**kwargs)
        context['content'] =  ContentForm()
        context['content_file']=''
        return context

    def form_valid(self, form):
        print (' valud save data after upload files  in Create Moment')        
        form_valid(self.request,form)
        return redirect(to='momentos_view')


class UpdateMomentView(LoginRequiredMixin, OnlyContentCreatorAndSupervisorMixin, UpdateView):
    """
    Update existing Momento view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/momentos-edit.html'
    form_class = MomentUpdateForm
    #second_form_class = ContentForm

    def get_object(self, queryset=None):
        return Moment.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(UpdateMomentView, self).get_context_data(**kwargs)
        get_context_data_update(self.object, context,**kwargs)
        content = Content.objects.get(pk=self.get_object().content.id)        
        context['content'] =  ContentForm(instance=content)
        context['content_file']=content.content.name
        return context



    def form_valid(self, form):
        form_valid(self.request,form)
        return redirect(to='momentos_view')


class DeleteMomentView(View):
    """
    Deletes Momento object
    """
    def dispatch(self, request, *args, **kwargs):
        Moment.objects.get(pk=self.kwargs['pk']).pre_delete()
        return redirect(to='momentos_view')


@method_decorator(xframe_options_exempt, name='dispatch')
class MomentView(DetailView):
    """
    Displays uploaded H5P package
    """
    template_name = 'packages/package_view.html'
    model = Moment
    context_object_name = 'package'

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs.keys():
            return self.model.objects.get(pk=self.kwargs['pk'])   
        else:
            raise ValueError('Neither pk nor moment_id were given as parameters')

    
