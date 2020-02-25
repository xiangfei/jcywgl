#coding=utf-8



class RESOURCE:

    # 脚手架
    initframe = [
        {'name':'project_name', 'nullable':False},
        {'name':'service_name', 'nullable':False},
        {'name':'project_type', 'nullable':False},
        {'name':'remark', 'nullable':True}
    ]

    listframe = [
        {'name':'page', 'nullable':True},
        {'name':'limit', 'nullable':True}
    ]

    # 项目
    project_list_params = [
        {'name':'page', 'nullable':True, 'default':1},
        {'name':'limit', 'nullable':True, 'default':20},
        {'name':'project_name', 'nullable':True},
        {'name':'department_id', 'nullable':True}
    ]

    project_add_params = [
        {'name':'project_name', 'nullable':False},
        {'name':'department_id', 'nullable':False},
        {'name':'project_stage', 'nullable':False},
        {'name':'leader_id', 'nullable':False},
        {'name':'desc', 'nullable':True}
    ]

    project_info_params = [
        {'name':'id', 'nullable':False}
    ]

    project_update_params = [
        {'name':'id', 'nullable':False},
        {'name':'project_name', 'nullable':False},
        {'name':'department_id', 'nullable':False},
        {'name':'project_stage', 'nullable':False},
        {'name':'leader_id', 'nullable':False},
        {'name':'desc', 'nullable':True}
    ]    

    project_delete_params = [
        {'name':'id', 'nullable':False}
    ]    

    # 模块
    module_list_params = [

    ]

    module_add_params = [
        {'name':'module_name', 'nullable':False},
        {'name':'project_id', 'nullable':False},
        {'name':'module_tech', 'nullable':False},
        {'name':'git_url', 'nullable':False},
        {'name':'logs_path', 'nullable':False},
        {'name':'module_path', 'nullable':True},
        {'name':'port', 'nullable':True},
        {'name':'desc', 'nullable':True},

        {'name':'module_type', 'nullable':True},
        {'name':'sequence', 'nullable':True}
    ]

    module_info_params = [

    ]

    module_update_params = [

    ]

    module_delete_params = [

    ]
