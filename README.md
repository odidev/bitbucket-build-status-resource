# concourse-resource-bitbucket

[![Docker Pulls](https://img.shields.io/docker/pulls/karunamon/concourse-resource-bitbucket.svg?maxAge=2592000)](https://hub.docker.com/r/karunamon/concourse-resource-bitbucket/)
[![Requirements Status](https://requires.io/github/Karunamon/concourse-resource-bitbucket/requirements.svg?branch=master)](https://requires.io/github/Karunamon/concourse-resource-bitbucket/requirements/?branch=master)
[![Build Status](https://travis-ci.org/Karunamon/concourse-resource-bitbucket.svg?branch=master)](https://travis-ci.org/Karunamon/concourse-resource-bitbucket)

This is a fork of https://github.com/Karunamon/concourse-resource-bitbucket.
The following forks have been merged in, too:
* https://github.com/Fydon/concourse-resource-bitbucket
* https://github.com/mehtaphysical/concourse-resource-bitbucket
* https://github.com/aecepoglu/concourse-resource-bitbucket
* https://github.com/ecometrica/concourse-resource-bitbucket
* https://github.com/Meshcloud/concourse-resource-bitbucket
This fork is substantially changed from the original.

Summary of changes:

* Targets bitbucket api version 2 instead of 1.
* Only targets bitbucket.org.
* Change auth from user/password to [OAuth client credentials grant](https://developer.atlassian.com/bitbucket/api/2/reference/meta/authentication).
* Support both hg and git repos.
* Create an automated docker build.
* Uses unittests instead of behave for tests.
* Post correct URLs to Bitbucket when using multiple teams in concourse

You can find a pre-built [Docker image on DockerHub](https://hub.docker.com/r/shyxormz/bitbucket-build-status-resource/).
If you come from one of the integrated forks, you can use the image with tag `compability`, which should work without you changing anything else.

## Creating an Access Token
You need to create an OAuth access token for your github team/user account with the following permissions: `Webhooks (r/w), Repositories (r)`

Make sure to **provide a callback URL** (it's not needed at runtime but Bitbucket insists on it anyway). For example, you can use the URL of your concourse instance. Otherwise you will see an error similar to the following
`
Access token result: <Response [400]>{"error_description": "No callback uri defined for the OAuth client.", "error": "invalid_request"}
HTTP 401 Unauthorized - Are your bitbucket credentials correct?
`


## Resource Configuration

These items go in the `source` fields of the resource type. Bold items are required:
 * `debug` - When True, dump the JSON documents sent and received for troubleshooting. (default: false)
 * `driver` - Are you using Bitbucket Cloud or Bitbucket Server. (default: Bitbucket Server)

### `Bitbucket Cloud` Driver
 * **`owner`** - The owner of the repository, which will either be a username or team
 * **`repository_name`** - The name of the repository on Bitbucket Cloud
 * **`client_id`** - Client id of the OAuth consumer. Shown as `Key` in the bitbucket interface.
 * **`secret`** - Secret for the OAuth consumer.
 * **`repo`** - Full repository name on bitbucket to set build status in. (`<username>/<reponame>`).

### `Bitbucket Server` Driver
* **`bitbucket_url`** - *base* URL of the bitbucket instance, including a trailing slash. (example: `https://bitbucket.mynetwork.com/`)
* **`bitbucket_user`** - Login username of someone with rights to the repository being updated.
* **`bitbucket_password`** - Password for the mentioned user. For Bitbucket Cloud this will need to be an [app password](https://confluence.atlassian.com/bitbucket/app-passwords-828781300.html) with permission to read from a repository and write to a repository.
* `verify_ssl` - When False, ignore any HTTPS connection errors if generated. Useful if on an internal network. (default: True)
## Behavior

### `check`

No-op

### `in`

No-op

### `out`

Update the status of a commit.

Parameters: *(items in bold are required)*

 * **`repo`** - Name of the git repo containing the SHA to be updated.
 This will come from a previous `get` on a `git/hg` resource.
 Make sure to use the git directory name, not the name of the resource.

 * **`state`** - the state of the status. Must be one of
 `SUCCESSFUL`, `FAILED`, or `INPROGRESS` - case sensitive.

 * `build_url_file` - Use the url given in file.

 * `key` - Use the given key in build notification.
 If different notifications have the same key, they will stack.

 * `name` - Use the given name in build notification.
 This will show up on bitbucket. For example "unit tests", "end to end tests"
 * `description_file` - A path to a file containing a description of the
 build. For example: "7 tests have failed"

## Example

A typical use case is to update the status of a commit as it traverses your pipeline.
The following example marks the commit as pending before unit tests start.
Once unit tests finish, the status is updated to either success or failure depending on how the task completes.

---
    resource_types:
      - name: bitbucket-notify
        type: docker-image
        source:
          repository: ecometrica/concourse-resource-bitbucket

    resources:
      - name: testing-repo
        type: git
        source:
          uri: https://bitbucket.org/someuser/somerepo.git
          branch: master

      - name: bitbucket-notify
        type: bitbucket-notify
        source:
          client_id: cid
          secret: hemligt
          repo: user/repo

    jobs:
      - name: integration-tests
        plan:
        - get: testing-repo
          trigger: true

        - put: bitbucket-notify
          params:
            state: INPROGRESS
            repo: testing-repo

        - task: tests
          file: testing-repo/task.yml
          on_success:
            put: bitbucket-notify
            params:
              state: SUCCESSFUL
              repo: testing-repo
          on_failure:
            put: bitbucket-notify
            params:
              state: FAILED
              repo: testing-repo

In this example, notice that the repo: parameter is set to the same name as the testing-repo resource.
To reiterate: **In your deployment, set the repo: field to the folder name of the git repo**, or in other words,
what you'd end up with if you ran a `git/hg clone` against the URI.

To install on all Concourse workers, update your deployment manifest properties to include a new `groundcrew.resource_types` entry...

    properties:
      groundcrew:
        additional_resource_types:
          - image: "docker:///karunamon/concourse-resource-bitbucket#master"
            type: "bitbucket-notify"

### Pipeline-specific

To use on a single pipeline, update your pipeline to include a new `resource_types` entry...

    resource_types:
      - name: "bitbucket-notify"
        type: "docker-image"
        source:
          repository: "karunamon/concourse-resource-bitbucket"
          tag: "master"

## Low hanging improvement fruit
This is a work in progress and there are multiple areas that could use some improvement.
Any contribution is welcomed.

* Need to specify the repo explicitly in the source parameters.
  Change this to read the correct remote url from the repo itself.
* Add back support for self hosted bitbuckets.
* Write more tests.

## References

 * [Resources (concourse.ci)](https://concourse.ci/resources.html)
 * [Bitbucket build status API](https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Busername%7D/%7Brepo_slug%7D/commit/%7Bnode%7D/statuses/build)

## Thanks
* [Karunamon](https://github.com/Karunamon) for getting the ball rolling.

## License

[Apache License v2.0]('./LICENSE')

