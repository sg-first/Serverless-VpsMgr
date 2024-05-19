from django.http import JsonResponse
import threading
import logging

vps_dict = {}  # vps_dict = {vps_id:{http_address:xxxx, vps_status:xxx}}
vps_dict_lock = threading.Lock()  # 全局锁

logger = logging.getLogger(__name__)


def search_available_vps(request):  # ws服务调这个函数。如果发现没有空闲的就不发通知了。让机器空闲之后自己去MQ上拉；有空闲的话就通知
    global vps_dict
    global vps_dict_lock

    logger.info("search_available_vps() called")

    vps_dict_lock.acquire()

    try:
        for vps_id, vps_info in vps_dict.items():
            if vps_info['bAvailable']:  # ==True
                logger.info(f"Found available VPS: {vps_id}")
                return JsonResponse({'vps_id': vps_id})
    finally:
        vps_dict_lock.release()  # 释放锁
        logger.info("Released vps_dict_lock")

    logger.info("No available VPS found")
    return JsonResponse({'vps_id': None})  # 返回None说明目前没有空闲的


def vps_update_status(request):  # 已经上报过的vps训练完了调用此函数把状态调至空闲(available)
    vps_dict_lock.acquire()  # 获取锁

    # 要获取这些元素：vps_id:{http_address:xxxx, vps_status:xxx}
    # 然后以键值对形式存入字典
    try:
        vps_id = request.POST.get('vps_id')
        if request.POST.get('msg_type') == 'finish_working':
            vps_dict[vps_id]['bAvailable'] = True
        else:  # == 'start_working'
            vps_dict[vps_id]['bAvailable'] = False
    finally:
        vps_dict_lock.release()  # 释放锁

    return JsonResponse({'status': 'success'})  # 返回一个合适的 JSON 响应


def vps_register(request):  # 首次上报
    vps_dict_lock.acquire()  # 获取锁
    try:
        vps_id = request.POST.get('vps_id')
        http_address = request.POST.get('http_address')
        vps_dict[vps_id] = {
            'http_address': http_address,
            'bAvailable': True  # 此时一定是空闲状态
        }
    finally:
        vps_dict_lock.release()  # 释放锁
    return JsonResponse({'status': 'success'})  # 返回一个合适的 JSON 响应
