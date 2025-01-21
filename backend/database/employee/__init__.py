from .employee_queries import insert_employee, update_employee_email, delete_employee, select_employee_by_id
from .application_queries import (
    insert_application, delete_application, select_all_specializations,
    select_all_applications_id_with_specialization, select_one_application_id,
    select_application_by_id, delete_applications_related_to_employee
)
from .like_queries import (insert_like, select_like_id, delete_like, delete_all_likes_by_employer_id,
delete_all_likes_by_employee_id)
