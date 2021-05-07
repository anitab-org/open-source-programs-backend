from rest_framework import routers

from osp.views.answer import AnswerView
from osp.views.form import FormView
from osp.views.form_feedback import FormFeedbackView
from osp.views.github_stat import GithubStatView
from osp.views.question import QuestionView
from osp.views.user import UserView
from osp.views.user_information import UserInformationView
from osp.views.zulip_stat import ZulipStatView

router = routers.DefaultRouter()

router.register(r"user", UserView, basename="user")
router.register(r"info", UserInformationView, basename="information")
router.register(r"form", FormView, basename="form")
router.register(r"questions", QuestionView, basename="questions")
router.register(r"answers", AnswerView, basename="answers")
router.register(r"feedback", FormFeedbackView, basename="form_feedback")
router.register(r"zulip_stat", ZulipStatView, basename="zulip_stat")
router.register(r"github_stat", GithubStatView, basename="github_stat")


urlpatterns = []

urlpatterns += router.urls
