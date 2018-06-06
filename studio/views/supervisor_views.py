from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, FormView

from alumnica_model.models import Ambit, users, Subject


class AproveToPublishDashboard(LoginRequiredMixin, ListView):
    login_url = "login_view"
    template_name = ""
    queryset = Ambit.objects.filter(is_draft=False, is_published=False)
    context_object_name = "ambits_2_aprove_list"

    def dispatch(self, request, *args, **kwargs):
        if request.user.type != users.TYPE_SUPERVISOR:
            return redirect(to="dashboard_view")
        else:
            return super(AproveToPublishDashboard, self).dispatch(self, request, *args, **kwargs)


class AmbitPreviewView(LoginRequiredMixin, DetailView):
    login_url = "login_view"
    template_name = ""

    def dispatch(self, request, *args, **kwargs):
        if request.user.type != users.TYPE_SUPERVISOR:
            return redirect(to="dashboard_view")
        else:
            return super(AmbitPreviewView, self).dispatch(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AmbitPreviewView, self).get_context_data(**kwargs)
        ambit = Ambit.objects.get(pk=kwargs['pk'])
        context.update({'ambit': ambit})
        return context


class GridPositionView(LoginRequiredMixin, FormView):
    login_url = "login_view"
    template_name = ""

    def dispatch(self, request, *args, **kwargs):
        if request.user.type != users.TYPE_SUPERVISOR:
            return redirect(to="dashboard_view")
        else:
            return super(GridPositionView, self).dispatch(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GridPositionView, self).get_context_data(**kwargs)
        ambits_list = Ambit.objects.filter(is_published=True)
        ambit = Ambit.objects.get(pk=kwargs['pk'])
        context.update({'ambits_list': ambits_list, 'new_ambit': ambit})

    def form_valid(self, form):
        position_array = self.request.POST.get('positions').split(';')
        for element in position_array:
            ambit_position = element.split(',')
            ambit = Ambit.objects.get(pk=ambit_position[0])
            ambit.position = ambit_position[1]
            ambit.save()
        return redirect(to="")


class OdasPositionSubjectPreview(LoginRequiredMixin, FormView):
    login_url = "login_view"
    template_name = ""

    def dispatch(self, request, *args, **kwargs):
        if request.user.type != users.TYPE_SUPERVISOR:
            return redirect(to="dashboard_view")
        else:
            return super(OdasPositionSubjectPreview, self).dispatch(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OdasPositionSubjectPreview, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        subject = Subject.objects.get(pk=self.kwargs['pk'])
        section_images_list = subject.sections_images.all()
        odas_list = []
        section_counter = 1
        for section in subject.sections_images.all():
            odas_list.append(subject.odas.all().filter(section=section_counter))
            section_counter += 1

        content_images = zip(odas_list, section_images_list)
        context.update({'content_images': content_images})
        return context

