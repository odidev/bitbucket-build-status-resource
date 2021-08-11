import subprocess
from behave import given, then


def good_dict():
    return {'source': {
                'bitbucket_url': 'https://test.bitbucket.local/',
                'debug': True,
                'username': 'ValidUser',
                'password': 'password',
            },
            'params': {
                'build_status': 'SUCCESSFUL'
            }
            }


def good_status_dict():
    build_url = "https://concourse.local/pipelines/testing/jobs/1/builds/1"
    return {
        "state": 'INPROGRESS',
        "key": "B-1",
        "name": "build",
        "url": build_url,
        "description": "Concourse build %s" % "ABC"
    }


@given(u'I have used the "in" script')
def step_impl(context):
    context.inscript = "scripts/in"


@then(u'I should get back an empty ref')
def step_impl(context):
    out = subprocess.check_output("python " + context.inscript, shell=True).strip()
    print("*******")
    print(str(out))

    assert str(b'{ "version": { "ref": "none" }}') == str(out)


@given(u'I have used the "check" script')
def step_impl(context):
    context.checkscript = "scripts/check"


@then(u'I should get back an empty array')
def step_impl(context):
    out = subprocess.check_output("python " + context.checkscript, shell=True).strip()
    assert "[]" in str(out)
