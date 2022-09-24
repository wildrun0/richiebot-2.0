from vkbottle.bot import Message
from handlers.peer_handler import PeerObject
from vkbottle import VKAPIError


async def renew_admin_list(event: Message, peers_obj: PeerObject):
    try:
        admins = (await event.ctx_api.messages.get_conversation_members(event.peer_id))
    except VKAPIError[917]: return
    adms = list(filter(None, [x.is_admin and x.member_id for x in admins.items]))
    peers_obj.data.admins = adms
    await peers_obj.save()
    
# chat_restrictions=None 
# count=4 groups=[
#     GroupsGroupFull(
#         admin_level=None, 
#         deactivated=None, 
#         est_date=None, 
#         finish_date=None, 
#         id=186022705, 
#         is_admin=None, 
#         is_advertiser=None, 
#         is_closed=<GroupsGroupIsClosed.open: 0>, 
#         is_member=None, 
#         is_video_live_notifications_blocked=None, 
#         name='coolbot', 
#     ), 
#     GroupsGroupFull(
#         admin_level=None, deactivated=None, est_date=None, finish_date=None, 
#         id=190597444, is_admin=None, is_advertiser=None, is_closed=<GroupsGroupIsClosed.open: 0>,
#         is_member=None, is_video_live_notifications_blocked=None, 
#         name='Бот Ричи'] 
#     items=[
#         MessagesConversationMember(
#             can_kick=None, 
#             invited_by=397717739, 
#             is_admin=True, 
#             is_message_request=None, 
#             is_owner=True, 
#             join_date=1606575768, 
#             member_id=397717739, 
#             request_date=None
#         ), 
#         MessagesConversationMember(
#             can_kick=True, 
#             invited_by=397717739, 
#             is_admin=None, 
#             is_message_request=None, 
#             is_owner=None, 
#             join_date=1597604976, 
#             member_id=320750004, 
#             request_date=None
#         ), 
#         MessagesConversationMember(
#             can_kick=None, 
#             invited_by=397717739,
#             is_admin=True, 
#             is_message_request=None, 
#             is_owner=None, 
#             join_date=1655377048, 
#             member_id=-186022705, 
#             request_date=None
#         ), 
#         MessagesConversationMember(
#             can_kick=None, 
#             invited_by=397717739, 
#             is_admin=True, 
#             is_message_request=None, 
#             is_owner=None, 
#             join_date=1657133939, 
#             member_id=-190597444, 
#             request_date=None)
#     ],
#     profiles=[
#         UsersUserFull(
#             can_access_closed=True, 
#             deactivated=None, 
#             first_name='Виктор', 
#             hidden=None, 
#             id=320750004, 
#             is_closed=False, 
#             last_name='Воробьев', 
#             friend_status=None, 
#             mutual=None, 
#             online=<BaseBoolInt.yes: 1>, 
#             online_app=None, 
#             online_info=UsersOnlineInfo(
#                 app_id=None, 
#                 is_mobile=False, 
#                 is_online=True, 
#                 last_seen=1664042164, 
#                 status=None, visible=True
#             ), 
#             online_mobile=None,
#             photo_100='&crop=535,644,690,690&ava=1', 
#             photo_50='https://sun1.sibirix.userapi.L_', 
#             screen_name='tgwalker', 
#             sex=<BaseSex.male: 2>, 
#             trending=None, 
#             verified=None, 
#             about=None, 
#             access_key=None, 
#             activities=None, 
#             activity=None, 
#             bdate=None, 
#             blacklisted=None, 
#             blacklisted_by_me=None, 
#             books=None, 
#             can_be_invited_group=None, can_call=None, can_call_from_group=None, can_post=None, can_see_all_posts=None, can_see_audio=None, can_see_gifts=None, can_see_wishes=None, can_send_friend_request=None, can_subscribe_podcasts=None, can_subscribe_posts=None, can_upload_doc=None, can_write_private_message=None, career=None, city=None, clips_count=None, common_count=None, contact_id=None, contact_name=None, counters=None, country=None, crop_photo=None, descriptions=None, domain=None, education_form=None, education_status=None, email=None, exports=None, facebook=None, facebook_name=None, faculty=None, faculty_name=None, first_name_abl=None, first_name_acc=None, first_name_dat=None, first_name_gen=None, first_name_ins=None, first_name_nom=None, followers_count=None, games=None, graduation=None, has_mobile=None, has_photo=None, has_unseen_stories=None, hash=None, home_phone=None, home_town=None, instagram=None, interests=None, is_favorite=None, is_friend=None, is_hidden_from_feed=None, is_message_request=None, is_no_index=None, is_service=None, is_subscribed_podcasts=None, is_video_live_notifications_blocked=None, language=None, last_name_abl=None, last_name_acc=None, last_name_dat=None, last_name_gen=None, last_name_ins=None, last_name_nom=None, last_seen=None, lists=None, livejournal=None, maiden_name=None, military=None, mobile_phone=None, movies=None, music=None, nickname=None, occupation=None, owner_state=None, personal=None, photo=None, photo_200=None, photo_200_orig=None, photo_400=None, photo_400_orig=None, photo_big=None, photo_id=None, photo_max=None, photo_max_orig=None, photo_max_size=None, photo_medium=None, photo_medium_rec=None, photo_rec=None, quotes=None, relation=None, relation_partner=None, relatives=None, schools=None, service_description=None, site=None, skype=None, status=None, status_audio=None, stories_archive_count=None, test=None, timezone=None, tv=None, twitter=None, type=None, universities=None, university=None, university_group_id=None, university_name=None, video_live=None, video_live_count=None, video_live_level=None, wall_comments=None, wall_default=None), UsersUserFull(can_access_closed=True, deactivated=None, first_name='Александр', hidden=None, id=397717739, is_closed=False, last_name='Постников', friend_status=None, mutual=None, online=<BaseBoolInt.yes: 1>, online_app=None, online_info=UsersOnlineInfo(app_id=None, is_mobile=False, is_online=True, last_seen=1664042166, status=None, visible=True), online_mobile=None, photo_100='https://sun1.sibirix.userapi.com/s/v1/ig2/ISpy5VixUC9WH4yHIK6MfxreQCCGbCFq_hjo18kQrUIFtCCwh9RSmOimv8dNS4O-UoVFCFpQPtKFJYWCZC1Hlicr.jpg?size=100x100&quality=95&crop=76,179,393,393&ava=1', photo_50='https://sun1.sibirix.userapi.com/s/v1/ig2/8p-gs3P27O9GVEgupX_0sFZv3whTyfibfnk-57M6irMeFmp4uRvaHDPFb4jmLO0oglhi_De98H8kN_W26T5LqBO3.jpg?size=50x50&quality=95&crop=76,179,393,393&ava=1', screen_name='wildrun0', sex=<BaseSex.male: 2>, trending=None, verified=None, about=None, access_key=None, activities=None, activity=None, bdate=None, blacklisted=None, blacklisted_by_me=None, books=None, can_be_invited_group=None, can_call=None, can_call_from_group=None, can_post=None, can_see_all_posts=None, can_see_audio=None, can_see_gifts=None, can_see_wishes=None, can_send_friend_request=None, can_subscribe_podcasts=None, can_subscribe_posts=None, can_upload_doc=None, can_write_private_message=None, career=None, city=None, clips_count=None, common_count=None, contact_id=None, contact_name=None, counters=None, country=None, crop_photo=None, descriptions=None, domain=None, education_form=None, education_status=None, email=None, exports=None, facebook=None, facebook_name=None, faculty=None, faculty_name=None, first_name_abl=None, first_name_acc=None, first_name_dat=None, first_name_gen=None, first_name_ins=None, first_name_nom=None, followers_count=None, games=None, graduation=None, has_mobile=None, has_photo=None, has_unseen_stories=None, hash=None, home_phone=None, home_town=None, instagram=None, interests=None, is_favorite=None, is_friend=None, is_hidden_from_feed=None, is_message_request=None, is_no_index=None, is_service=None, is_subscribed_podcasts=None, is_video_live_notifications_blocked=None, language=None, last_name_abl=None, last_name_acc=None, last_name_dat=None, last_name_gen=None, last_name_ins=None, last_name_nom=None, last_seen=None, lists=None, livejournal=None, maiden_name=None, military=None, mobile_phone=None, movies=None, music=None, nickname=None, occupation=None, owner_state=None, personal=None, photo=None, photo_200=None, photo_200_orig=None, photo_400=None, photo_400_orig=None, photo_big=None, photo_id=None, photo_max=None, photo_max_orig=None, photo_max_size=None, photo_medium=None, photo_medium_rec=None, photo_rec=None, quotes=None, relation=None, relation_partner=None, relatives=None, schools=None, service_description=None, site=None, skype=None, status=None, status_audio=None, stories_archive_count=None, test=None, timezone=None, tv=None, twitter=None, type=None, universities=None, university=None, university_group_id=None, university_name=None, video_live=None, video_live_count=None, video_live_level=None, wall_comments=None, wall_default=None)]