from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from .models import SingleQuestion

class SingleQuestionAdmin(ModelAdmin):
    model = SingleQuestion
    menu_label = 'Questions'  # ditch this to use verbose_name_plural from model
    menu_icon = 'help'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('question_text', 'category', 'correct_ans')
    # list_filter = ('live', 'example_field2', 'example_field3')
    # search_fields = ('title',)

class AssessmentAdminGroup(ModelAdminGroup):
    items = (SingleQuestionAdmin,)

modeladmin_register(AssessmentAdminGroup)
