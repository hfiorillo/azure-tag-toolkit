import requests, json
# from getpass import getpass
print('This is the Azure Tagging Toolkit and provides the following functionality...')
print('')
print('Update tag keys, update tag values, add tags and delete tags across an Azure environment.')
print('')

# Include resources or resource groups
include_resource_groups = input('Do you want to include resource groups? If so type "yes": ')
if include_resource_groups == 'yes':
    include_resource_groups == True
else:
    include_resource_groups == False

include_resources = input('Do you want to include resources? If so type "yes": ')
if include_resources == 'yes':
    include_resources == True
else:
    include_resources == False

# Setting Validation

if not include_resource_groups and include_resources:
    print('You must include resources or resource groups for the script to do something')
    exit()

print('We will now collect some details... Please ensure you have a service principal created.')
print('')

# Inputs from user
tenant_id = input('Tenant ID: ') 
if len(tenant_id) < 1:
    print('Tenant ID is required for this script')
    print('Exiting...')
    exit()
client_id = input('Client ID: ')
if len(client_id) < 1:
    print('Client ID is required for this script')
    print('Exiting...')
    exit()
client_secret = input('Client Secret: ') # can use getpass
if len(client_secret) < 1:
    print('Client Secret is required for this script')
    print('Exiting...')
    exit()

def validate(x):
    if len(x) < 1 or len(x) > 16:
        print('Tags must be at least 1 character but less than 16 characters')
        print('Exiting...')
        exit()

print('')
print('')
toolkit_choice = input('Please enter what you want to modify? Select from: keys, values, add or delete \n')
if toolkit_choice == 'keys':
    print('')
    print('Lets begin...')
    old_key = input('Old key: ')
    validate(old_key)
    new_key = input('New key: ')
    validate(new_key)
if toolkit_choice == 'values':
    print('')
    print('Lets begin...')
    key_value = input('Key for the value: ')
    validate(key_value)
    new_value = input('New value for the tag: ')
    validate(new_value)
if toolkit_choice == 'add':
    print('')
    print('Lets begin...')
    key_value = input('New key for the tag: ')
    validate(key_value)
    new_value = input('New value for the tag: ')
    validate(new_value)
if toolkit_choice == 'delete':
    print('')
    print('Lets begin... Please enter each tag you want deleting seperated by a comma (case sensitive).')
    tag_list = input('Old tag(s): ')
    del_tags = list(tag_list.split(','))
    print('')
    

# Toolkit choice
print('Please specify which part of the toolkit you require...')
toolkit_update_key = input('Do you want to update tag keys? If so type yes: ')
if toolkit_update_key == 'yes':
    print('')
    print('Lets begin...')
    old_key = input('Old key: ')
    validate(old_key)
    new_key = input('New key: ')
    validate(new_key)

toolkit_update_value = input('Do you want to update tag values? If so type yes: ')
if toolkit_update_value == 'yes':
    print('')
    print('Lets begin...')
    key_value = input('Key for the value: ')
    validate(key_value)
    new_value = input('New value for the tag: ')
    validate(new_value)

toolkit_add_tag = input('Do you want to add new tags? If so type yes: ')
if toolkit_add_tag == 'yes':
    print('')
    print('Lets begin...')
    tag_key = input('New tag key: ')
    validate(tag_key)
    tag_value = input('New tag value: ')
    validate(tag_value)

toolkit_del_tag = input('Do you want to delete tags? If so type yes: ')
if toolkit_del_tag == 'yes':
    print('')
    print('Lets begin... Please enter each tag you want deleting seperated by a comma (case sensitive).')
    tag_list = input('Old tag(s): ')
    del_tags = list(tag_list.split(','))
    print('')

# Global Variable
base_url = 'https://management.azure.com'

## Authenticate against azure function
def authenticate(tenant_id, client_id, client_secret):
    auth_url = 'https://login.microsoftonline.com/' + tenant_id + '/oauth2/token'
    auth_payload = 'grant_type=client_credentials&resource=https%3A%2F%2Fmanagement.azure.com&client_id=' + client_id + '&client_secret=' + client_secret
    print('Authenticating')
    auth_response = requests.request('POST', auth_url, headers={ 
        'Content-Type': 'application/x-www-form-urlencoded'
    }, data=auth_payload)
    auth_json_response = json.loads(auth_response.text)
    if not 'token_type' in auth_json_response or not 'access_token' in auth_json_response:
        print('Authentication failed... Please check your service principal details are correct.')
        print('Exiting...')
        exit()
    auth_token = auth_json_response['token_type'] + ' ' + auth_json_response['access_token']
    if 'Bearer ' in auth_token:
        print('Authenticated')
    return auth_token

## Get subscriptions from azure
def getSubscriptions(auth_token):
    subscriptions_url = base_url + '/subscriptions?api-version=2020-01-01'
    print('Checking what subscriptions you have access to')
    all_subscriptions = []
    subscriptions_response = requests.request('GET', subscriptions_url, headers={
        'Authorization': auth_token
    }, data={})
    for subscription in json.loads(subscriptions_response.text)['value']:
        all_subscriptions.append(subscription['displayName'])
    print(str(len(all_subscriptions)) + 'subscription(s) found: \n' + ', '.join(all_subscriptions))
    print('')
    print('')
    return subscriptions_response.text

## Get resources from azure 
def getResources(subscription_id, getGroups, auth_token):
    url = base_url + '/subscriptions/' + subscription_id + '/resource'
    if getGroups:
        url = url + 'groups'
    else:
        url = url + 's'
    url = url + '?api-version=2020-06-01'
    resources_response = requests.request('GET', url, headers={
        'Authorization': auth_token
    }, data={})
    return resources_response.text

## Update tags
def updateTags(resourceId, tags, auth_token):
    resource_url = base_url + resourceId + '/providers/Microsoft.Resources/tags/default?api-version=2019-10-01'

    data = {
        'operation': 'replace',
        'properties': {
            'tags': tags
        }
    }
    body = json.dumps(data)
    tag_update_response = requests.request('PATCH', resource_url, headers={
        'Content-Type': 'application/json',
        'Authorization': auth_token
    }, data=body)
    return tag_update_response.text

# Functions
def complete():
    print('Running')
    for resource in tag_requests:
        resource_json = json.loads(resource)
        updateTags(resource_json['id'], resource_json['tags'], auth_token)
    message = ' resources'
    if include_resource_groups:
        message = message + '/resource groups'
    print(str(len(tag_requests)) + message + ' tags have been updated')

def tagRequests():
    tag_requests.append(json.dumps({
                    'id': resource['id'],
                    'tags': tags
                }))
                

# Tasks
print('')
print('')
print('')
auth_token = authenticate(tenant_id, client_id, client_secret)
subscriptions_response = getSubscriptions(auth_token);
subscriptions_json_response = json.loads(subscriptions_response)
tag_requests = []
for subscription in subscriptions_json_response['value']:
    subscription_id = subscription['subscriptionId']
    print('Getting resources from ' + subscription['displayName'] + ' - ' + subscription_id)
    print('')
    resource_response = getResources(subscription_id, include_resources, auth_token)
    resource_json_response = json.loads(resource_response)
    if not include_resources and include_resource_groups:
        print('Getting resource groups from ' + subscription['displayName'] + ' - ' + subscription_id)
        print('')
        resource_group_response = getResources(subscription_id, True, auth_token)
        resource_group_json_response = json.loads(resource_group_response)
        resource_json_response['value'] = resource_json_response['value'] + resource_group_json_response['value']
    
    if toolkit_update_key == 'yes':
        for resource in resource_json_response['value']:
            if resource and 'tags' in resource and old_key in resource['tags']:
                tags = resource['tags']
                print(tags)
                tags[new_key] = tags[old_key]
                print(tags)
                del tags[old_key]
                tagRequests()
        complete()

    if toolkit_add_tag == 'yes':
        for resource in resource_json_response['value']:
            if resource and 'tags' in resource:
                tags = resource['tags']
                tags.update({str(tag_key):str(tag_value)})
                tagRequests()
        complete()

    if toolkit_update_value == 'yes':
        for resource in resource_json_response['value']:
            if resource and 'tags' in resource:
                tags = resource['tags']
                tags[key_value] = new_value
                tagRequests()
        complete()

    if toolkit_del_tag == 'yes':
        for resource in resource_json_response['value']:
            if resource and 'tags' in resource:
                tags = resource['tags']
                tags_to_remove = del_tags
                for tag in del_tags:
                    if tag in tags:
                        del tags[tag]
                    tagRequests()
        complete()