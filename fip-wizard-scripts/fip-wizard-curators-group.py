import os

import dotenv
import requests


dotenv.load_dotenv()


class FIPWizardCuratorsGroup:

    PERM_TYPES = {
        'UserMember': 'UserQuestionnairePermType',
        'UserGroupMember': 'UserGroupQuestionnairePermType',
    }

    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key
        self._session = requests.Session()
        self._session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
        })

    def get_projects(self):
        response = self._session.get(
            url=f'{self.api_url}/questionnaires',
            params={
                'size': 5000,
                'sort': 'createdAt,desc',
            },
        )
        response.raise_for_status()
        return response.json().get('_embedded', {}).get('questionnaires', [])

    def get_project(self, project_uuid):
        response = self._session.get(
            url=f'{self.api_url}/questionnaires/{project_uuid}/questionnaire',
        )
        response.raise_for_status()
        return response.json()

    def update_share(self, project_uuid, group_uuid, perms):
        data = self.get_project(project_uuid)

        permissions = []
        for perm_item in data.get('permissions', []):
            member = perm_item.get('member', {})
            member_uuid = member['uuid']
            if member_uuid == group_uuid:
                continue
            permissions.append({
                'memberType': self.PERM_TYPES[member['type']],
                'memberUuid': member['uuid'],
                'perms': perm_item['perms'],
            })
        permissions.append({
            'memberType': self.PERM_TYPES['UserGroupMember'],
            'memberUuid': group_uuid,
            'perms': perms,
        })
        share_data = {
            'permissions': permissions,
            'sharing': data['sharing'],
            'visibility': data['visibility'],
        }

        response = self._session.put(
            url=f'{self.api_url}/questionnaires/{project_uuid}/share',
            json=share_data,
        )
        response.raise_for_status()
        return response.json()


if __name__ == '__main__':
    api_url = os.getenv('WIZARD_API_URL')
    api_key = os.getenv('WIZARD_API_KEY')

    group_uuid = '8735311d-3413-482a-9933-318c7f6406cb'
    perms = ['VIEW', 'COMMENT', 'EDIT']

    if not api_url or not api_key:
        raise ValueError('API URL and API Key must be set in environment variables.')

    fip_wizard = FIPWizardCuratorsGroup(
        api_url=api_url,
        api_key=api_key,
    )
    projects = fip_wizard.get_projects()

    updated = 0
    for project in projects:
        permissions = {}
        for item in project.get('permissions', []):
            permissions[item['member']['uuid']] = item['perms']

        need_update = False
        if group_uuid not in permissions:
            need_update = True
        elif permissions[group_uuid] != perms:
            need_update = True

        if need_update:
            print(f'{project["uuid"]} = adding group {group_uuid}')
            fip_wizard.update_share(
                project_uuid=project['uuid'],
                group_uuid=group_uuid,
                perms=perms,
            )
            updated += 1
        else:
            print(f'{project["uuid"]} = {group_uuid} is already there (skipping)')

    print('-' * 80)
    print(f'Group added/updated in {updated} projects')
