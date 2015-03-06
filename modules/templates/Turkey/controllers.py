# -*- coding: utf-8 -*-

from gluon import *
from s3 import S3CustomController

THEME = "Turkey"

# =============================================================================
class index(S3CustomController):
    """ Custom Home Page """

    def __call__(self):

        output = {}

        # Allow editing of page content from browser using CMS module
        if current.deployment_settings.has_module("cms"):
            system_roles = current.auth.get_system_roles()
            ADMIN = system_roles.ADMIN in current.session.s3.roles
            s3db = current.s3db
            table = s3db.cms_post
            ltable = s3db.cms_post_module
            module = "default"
            resource = "index"
            query = (ltable.module == module) & \
                    ((ltable.resource == None) | \
                     (ltable.resource == resource)) & \
                    (ltable.post_id == table.id) & \
                    (table.deleted != True)
            item = current.db(query).select(table.body,
                                            table.id,
                                            limitby=(0, 1)).first()
            if item:
                if ADMIN:
                    item = DIV(XML(item.body),
                               BR(),
                               A(current.T("Edit"),
                                 _href=URL(c="cms", f="post",
                                           args=[item.id, "update"]),
                                 _class="action-btn"))
                else:
                    item = DIV(XML(item.body))
            elif ADMIN:
                if current.response.s3.crud.formstyle == "bootstrap":
                    _class = "btn"
                else:
                    _class = "action-btn"
                item = A(current.T("Edit"),
                         _href=URL(c="cms", f="post", args="create",
                                   vars={"module": module,
                                         "resource": resource
                                         }),
                         _class="%s cms-edit" % _class)
            else:
                item = ""
        else:
            item = ""
        output["item"] = item
        T = current.T

        self._view(THEME, "index.html")
        current.response.s3.stylesheets.append("../themes/CERT/homepage.css")

        title = current.deployment_settings.get_system_name()

        menus = [{"title":T("Organizations"),
                  "icon":"sitemap",
                  "description":T("Non-governmental organizations, community groups and government agencies and other disaster management stakeholders."),
                  "module":"org",
                  "function":"organisation",
                  "buttons":[{"args":"summary",
                              "icon":"list",
                              "label":T("View"),
                             },
                             {"args":"create",
                              "icon":"plus-sign",
                              "label":T("Create"),
                             }]
                  },
                 {"title":T("Offices"),
                  "icon":"building",
                  "description":T("The offices of organizations, their addresses and contact details."),
                  "module":"org",
                  "function":"office",
                  "buttons":[{"args":"summary",
                              "icon":"list",
                              "label":T("View"),
                             },
                             {"args":"create",
                              "icon":"plus-sign",
                              "label":T("Create"),
                             }]
                  },
                 {"title":T("Resources"),
                  "icon":"wrench",
                  "description":T("The resources such as tools and equipment available to organizations and neighborhoods to support disaster management activities."),
                  "module":"org",
                  "function":"resource",
                  "buttons":[{"args":"summary",
                              "icon":"list",
                              "label":T("View"),
                             },
                             {"args":"create",
                              "icon":"plus-sign",
                              "label":T("Create"),
                             }]
                  },
                 {"title":T("Projects"),
                  "icon":"map-marker",
                  "description":T("The details and locations of projects carried out by organizations."),
                  "module":"project",
                  "function":"project",
                  "buttons":[{"args":"summary",
                              "icon":"list",
                              "label":T("View"),
                             },
                             {"args":"create",
                              "icon":"plus-sign",
                              "label":T("Create"),
                             }]
                  },
                 {"title":T("Staff"),
                  "icon":"user",
                  "description":T("The staff working for organizations and information on their contact details and trainings."),
                  "module":"hrm",
                  "function":"staff",
                  "buttons":[{"args":"summary",
                              "icon":"list",
                              "label":T("View"),
                             },
                             {"args":"create",
                              "icon":"plus-sign",
                              "label":T("Create"),
                             }]
                  },
                 {"title":T("Volunteers"),
                  "icon":"group",
                  "description":T("The volunteers supporting organizations and information on their contact details and trainings."),
                  "module":"vol",
                  "function":"volunteer",
                  "buttons":[{"args":"summary",
                              "icon":"list",
                              "label":T("View"),
                             },
                             {"args":"create",
                              "icon":"plus-sign",
                              "label":T("Create"),
                             }]
                  },
                 {"title":T("Camps"),
                  "icon":"home",
                  "description":T("The details and locations of camps providing shelter to people displaced by disasters and refugees, including registration of people in camps."),
                  "module":"cr",
                  "function":"shelter",
                  "buttons":[{"args":"summary",
                              "icon":"list",
                              "label":T("View"),
                             },
                             {"args":"create",
                              "icon":"plus-sign",
                              "label":T("Create"),
                             }]
                  },
                 {"title":T("Main Map"),
                  "icon":"globe",
                  "description":T("The Main Sahana Map displays multiple layers of information from Sahana and external sources."),
                  "module":"gis",
                  "function":"Index",
                  "args":None,
                  "buttons":[]
                  },
                 ] 

        return dict(title = title,
                    menus=menus,
                    )


# END =========================================================================
