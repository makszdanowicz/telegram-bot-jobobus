from .employer_queries import insert_employer, change_employer_company_name, select_employer_by_id, delete_employer
from .job_offers_queries import (insert_job_offer, select_job_offer_by_id, delete_job_offer, 
select_all_job_offers, update_job_offer_description, select_all_specializations,
select_job_offer_by_id, select_job_offer_by_user_id, select_user_id_by_offer_id, select_matching_job_offers)
from .notification_queries import (insert_notification, count_unread_likes_for_employer,
    select_oldest_unread_likes_for_employer,
    change_notification_status, select_candidate_email_by_notification_id, delete_notification, delete_all_notifications_by_user_id,
    delete_all_notifications_by_employee_id)