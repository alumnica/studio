from django.contrib import admin
from studio.models import WorldModel, SubworldModel, ODAModel, ThemeModel, \
    EnigmaComicModel, EnigmaComicClickableAreaModel, EngimaComicStaticSceneModel, \
    EnigmaComicS360SceneModel, InteractiveVideoModel, VideoNodeModel, ForkNodeModel, NodeLinkModel, \
    LearnerEvaluationModel, QuestionModel, PossibleAnswerModel, AnswerGivenByLearnerModel, AdministratorModel, \
    ContentCreatorModel, DataAnalystModel, LearnerModel, ExerciseModel, ExerciseSolutionModel, UserModel
from studio.models.geometry import Point2DModel


admin.site.register(WorldModel)
admin.site.register(ThemeModel)
admin.site.register(SubworldModel)
admin.site.register(ODAModel)
admin.site.register(ExerciseModel)
admin.site.register(ExerciseSolutionModel)
admin.site.register(EnigmaComicModel)
admin.site.register(EnigmaComicClickableAreaModel)
admin.site.register(EngimaComicStaticSceneModel)
admin.site.register(EnigmaComicS360SceneModel)
admin.site.register(InteractiveVideoModel)
admin.site.register(VideoNodeModel)
admin.site.register(ForkNodeModel)
admin.site.register(NodeLinkModel)
admin.site.register(Point2DModel)
admin.site.register(LearnerEvaluationModel)
admin.site.register(QuestionModel)
admin.site.register(PossibleAnswerModel)
admin.site.register(AnswerGivenByLearnerModel)
admin.site.register(AdministratorModel)
admin.site.register(ContentCreatorModel)
admin.site.register(DataAnalystModel)
admin.site.register(LearnerModel)
