import json

from django.urls import reverse_lazy
from django.utils.datastructures import OrderedSet
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import FormView, DetailView, TemplateView

from django_h5p.forms import H5PackageForm
from django_h5p.models import H5Package


class UploadH5PackageView(FormView):
    form_class = H5PackageForm
    success_url = reverse_lazy('upload_h5p_view')
    template_name = 'django_h5p/upload_h5p_form.html'

    def get_context_data(self, **kwargs):
        context = super(UploadH5PackageView, self).get_context_data(**kwargs)
        context.update({
            'packages': H5Package.objects.all()
        })
        return context

    def form_valid(self, form):
        form.save()
        return super(UploadH5PackageView, self).form_valid(form)


@method_decorator(xframe_options_exempt, name='dispatch')
class PackageView(DetailView):
    template_name = 'django_h5p/package_view.html'
    model = H5Package
    context_object_name = 'package'

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs.keys():
            return self.model.objects.get(pk=self.kwargs['pk'])
        elif 'job_id' in self.kwargs.keys():
            return self.model.objects.get(job_id=self.kwargs['job_id'])
        else:
            raise ValueError('Neither pk nor job_id were given as parameters')

    def get_context_data(self, **kwargs):
        context = super(PackageView, self).get_context_data(**kwargs)

        context.update({
            'library_directory_name': self.object.main_library.full_name,
            'content_json': json.dumps(self.object.content, ensure_ascii=False),
            'stylesheets': list(OrderedSet({
                css for lib in self.object.preloaded_dependencies.all()
                for css in lib.get_all_stylesheets()
            })),
            'scripts': list(OrderedSet([
                script for lib in self.object.preloaded_dependencies.all()
                for script in lib.get_all_javascripts()
            ]))
        })

        return context


class ThreeSixtyView(TemplateView):
    template_name = 'django_h5p/365_test.html'
