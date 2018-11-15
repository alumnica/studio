import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studio_webapp.settings")

application = get_wsgi_application()
import time
from studio.forms.oda_forms import set_evaluation
from studio_webapp.settings import BASE_DIR
from random import randint
from django.core.files import File
from django.core.files.images import ImageFile
from model_mommy.recipe import Recipe, foreign_key, related
from alumnica_model.models.content import MicroODAType, Image, Evaluation, Moment, Ambit, Subject, ODA, MomentType
from alumnica_model.models.h5p import H5Package
from django_h5p.forms import H5PackageForm
from alumnica_model.models.users import TYPE_CONTENT_CREATOR

def get_h5p_package():
    packages = H5Package.objects.all()
    package = File(file=open(os.path.join(BASE_DIR, 'studio/tests/agamotto.h5p'), 'rb'))
    form = H5PackageForm(None, {'package': package})
    if form.is_valid():
        job = form.save()

        while not H5Package.objects.filter(job_id=job.id).exists():
            pass
        time.sleep(10)
        return '{}'.format(job.id)
    else:
        return False


def create_content(subjects, ambits):

    ambit_index = 0
    subjects_section_imgs = [Image.objects.create(name='subject_section_image',
                                                  folder="Materias",
                                                  file=ImageFile(
                                                      file=open(
                                                          os.path.join(BASE_DIR, 'studio/tests/subject_section1.png'),
                                                          'rb'))),
                             Image.objects.create(name='subject_section_image',
                                                  folder="Materias",
                                                  file=ImageFile(
                                                      file=open(
                                                          os.path.join(BASE_DIR, 'studio/tests/subject_section2.png'),
                                                          'rb'))),
                             Image.objects.create(name='subject_section_image',
                                                  folder="Materias",
                                                  file=ImageFile(
                                                      file=open(
                                                          os.path.join(BASE_DIR, 'studio/tests/subject_section3.png'),
                                                          'rb')))
                             ]
    oda_icons = [Image.objects.create(name='oda_active_icon', folder="ODAs", file=ImageFile(
        file=open(os.path.join(BASE_DIR, 'studio/tests/active_icon.gif'), 'rb'))), Image.objects.create(name='oda_completed_icon', folder="ODAs", file=ImageFile(
        file=open(os.path.join(BASE_DIR, 'studio/tests/completed_icon.gif'), 'rb')))]
    subject_section1 = subjects_section_imgs[0]
    subject_section2 = subjects_section_imgs[1]
    subject_section3 = subjects_section_imgs[2]
    microoda_types = list(MicroODAType.objects.all())

    for ambit in ambits[0:3]:
        ambit_recipe = Recipe(Ambit,
                              name=ambit['name'],
                              background_image=ambit['bck_image'],
                              position=ambit['position'],
                              color=ambit['color'],
                              is_published=True,
                              is_draft=False,
                              badge__first_version=ambit['badges'][0],
                              badge__second_version=ambit['badges'][1],
                              badge__third_version=ambit['badges'][2],
                              created_by__user_type=TYPE_CONTENT_CREATOR)

        ambit_mk = ambit_recipe.make(make_m2m=True,  _create_files=True)

        for subject in subjects[ambit_index]:

            subject_recipe = Recipe(Subject,
                                    name=subject['name'],
                                    background_image=subject['back_img'],
                                    temporal=False,
                                    number_of_sections=3,
                                    ambit=ambit_mk,
                                    created_by__user_type=TYPE_CONTENT_CREATOR
                                    )

            subject_mk = subject_recipe.make(_create_files=True)
            subject_mk.sections_images.add(subject_section1, subject_section2, subject_section3)

            for number in range(1, 4):
                evaluation_instance = Evaluation.objects.create(name='evaluation', folder='evaluations', file=File(
                                                 file=open(os.path.join(BASE_DIR, 'studio/tests/evaluation.xlsx'),
                                                           'rb')))

                set_evaluation(evaluation_instance)

                oda_recipe = Recipe(ODA,
                                    active_icon=oda_icons[0],
                                    completed_icon=oda_icons[1],
                                    zone=randint(1, 16),
                                    section=randint(1, 3),
                                    evaluation=evaluation_instance,
                                    temporal=False,
                                    subject=subject_mk,
                                    created_by__user_type=TYPE_CONTENT_CREATOR)

                oda_mk = oda_recipe.make(make_m2m=True,  _create_files=True)

                for type in microoda_types:
                    moment = Recipe(Moment,
                                    h5p_package=H5Package.objects.get(job_id=get_h5p_package()),
                                    microoda__type=type,
                                    microoda__oda=oda_mk,
                                    type=MomentType.objects.first(),
                                    created_by__user_type=TYPE_CONTENT_CREATOR)
                    moment.make(make_m2m=True,  _create_files=True)
        ambit_index += 1


ambit_bck_images = [Image.objects.create(name='ambit_back_image',
                           folder="Ambitos",
                           file=ImageFile(
                               file=open(os.path.join(BASE_DIR, 'studio/tests/ambito1.png'), 'rb'))),
                    Image.objects.create(name='ambit_back_image',
                           folder="Ambitos",
                           file=ImageFile(
                               file=open(os.path.join(BASE_DIR, 'studio/tests/ambito2.png'), 'rb')))
                    ]

ambit_badge_imgs = [Image.objects.create(name='ambit_badge_image',
                           folder="Ambitos",
                           file=ImageFile(
                               file=open(os.path.join(BASE_DIR, 'studio/tests/badge1.png'), 'rb'))),
                    Image.objects.create(name='ambit_badge_image',
                           folder="Ambitos",
                           file=ImageFile(
                               file=open(os.path.join(BASE_DIR, 'studio/tests/badge2.png'), 'rb'))),
                    Image.objects.create(name='ambit_badge_image',
                           folder="Ambitos",
                           file=ImageFile(
                               file=open(os.path.join(BASE_DIR, 'studio/tests/badge3.png'), 'rb')))
                    ]

ambits = [{'name': 'Propedeutico de ciencias', 'color': 'amarillo', 'position': 1, 'bck_image': ambit_bck_images[1],
           'badges': ambit_badge_imgs},
          {'name': 'Pensamiento matematico', 'color': 'rojiso', 'position': 2, 'bck_image': ambit_bck_images[0],
           'badges': ambit_badge_imgs},
          {'name': 'Métodos científicos experimentales', 'color': 'azul', 'position': 3,
           'bck_image': ambit_bck_images[1],
           'badges': ambit_badge_imgs},
          {'name': 'Desarrollo Humano', 'color': 'naranja', 'position': 4, 'bck_image': ambit_bck_images[0],
           'badges': ambit_badge_imgs},
          {'name': 'Historia y Sociedad', 'color': 'morado', 'position': 5, 'bck_image': ambit_bck_images[1],
           'badges': ambit_badge_imgs},
          {'name': 'Propedéutico lenguaje', 'color': 'bluegreen', 'position': 6, 'bck_image': ambit_bck_images[0],
           'badges': ambit_badge_imgs},
          {'name': 'Comunicación y Lenguaje', 'color': 'amarillo-sol', 'position': 7, 'bck_image': ambit_bck_images[1],
           'badges': ambit_badge_imgs},
          {'name': 'Pensamiento artístico', 'color': 'naranja-obscuro', 'position': 8, 'bck_image': ambit_bck_images[0],
           'badges': ambit_badge_imgs},
          {'name': 'Propedéutico Persona del Siglo XXI', 'color': 'violeta', 'position': 9,
           'bck_image': ambit_bck_images[1],
           'badges': ambit_badge_imgs},
          {'name': 'Herramientas de autogestión', 'color': 'azul-obscuro', 'position': 10,
           'bck_image': ambit_bck_images[0],
           'badges': ambit_badge_imgs},
          {'name': 'Tecnología digital', 'color': 'verde', 'position': 11, 'bck_image': ambit_bck_images[1],
           'badges': ambit_badge_imgs}
          ]

subjects_bck_imgs = [Image.objects.create(name='subject_back_image',
                            folder="Materias",
                            file=ImageFile(
                                file=open(os.path.join(BASE_DIR, 'studio/tests/subject1.png'), 'rb'))),
                    Image.objects.create(name='subject_back_image',
                            folder="Materias",
                            file=ImageFile(
                                file=open(os.path.join(BASE_DIR, 'studio/tests/subject2.png'), 'rb'))),
                    Image.objects.create(name='subject_back_image',
                            folder="Materias",
                            file=ImageFile(
                                file=open(os.path.join(BASE_DIR, 'studio/tests/subject3.png'), 'rb')))
                     ]


subjects = [[{'name': 'Epistemología', 'back_img': subjects_bck_imgs[0]},
             {'name': 'Métodos de investigación científica',
              'back_img': subjects_bck_imgs[1]}],
            [{'name': 'Álgebra', 'back_img': subjects_bck_imgs[0]},
             {'name': 'Geometría y trigonometría', 'back_img': subjects_bck_imgs[1]},
             {'name': 'Tratamiento de la información',
              'back_img': subjects_bck_imgs[2]}],
            [{'name': 'Modelos químicos', 'back_img': subjects_bck_imgs[0]},
             {'name': 'Leyes de la física', 'back_img': subjects_bck_imgs[1]},
             {'name': 'Sistemas biológicos', 'back_img': subjects_bck_imgs[2]},
             {'name': 'Geografía humana', 'back_img': subjects_bck_imgs[0]}],
            [{'name': 'Lógica', 'back_img': subjects_bck_imgs[0]},
             {'name': 'Ética y valores', 'back_img': subjects_bck_imgs[1]},
             {'name': 'Cosmovisiones fisiológicas',
              'back_img': subjects_bck_imgs[2]}],
            [{'name': 'Acontecimientos históricos',
              'back_img': subjects_bck_imgs[0]},
             {'name': 'Sociología económica', 'back_img': subjects_bck_imgs[1]},
             {'name': 'Derecho y sociedad', 'back_img': subjects_bck_imgs[2]}],
            [{'name': 'Etimologías mexicanas y grecolatinas',
              'back_img': subjects_bck_imgs[0]},
             {'name': 'Lenguaje simbólico', 'back_img': subjects_bck_imgs[1]}],
            [{'name': 'Ortografía', 'back_img': subjects_bck_imgs[0]},
             {'name': 'Redacción', 'back_img': subjects_bck_imgs[1]},
             {'name': 'Argumentación', 'back_img': subjects_bck_imgs[2]}],
            [{'name': 'Corrientes artísticas', 'back_img': subjects_bck_imgs[0]},
             {'name': 'Apreciación estética', 'back_img': subjects_bck_imgs[1]},
             {'name': 'Comunicaciñon visual', 'back_img': subjects_bck_imgs[2]}],
            [{'name': 'Sociedad del conocimiento', 'back_img': subjects_bck_imgs[0]},
             {'name': 'Cambio y empoderamiento social',
              'back_img': subjects_bck_imgs[1]}],
            [{'name': 'Finanzas personales', 'back_img': subjects_bck_imgs[0]},
             {'name': 'Derechos y obligaciones personales',
              'back_img': subjects_bck_imgs[1]},
             {'name': 'Talento personal', 'back_img': subjects_bck_imgs[2]}],
            [{'name': 'Productos de ofimática', 'back_img': subjects_bck_imgs[0]},
             {'name': 'Producción de identidad visual',
              'back_img': subjects_bck_imgs[1]},
             {'name': 'Inventos tecnológicos', 'back_img': subjects_bck_imgs[2]}]]

create_content(ambits=ambits, subjects=subjects)
