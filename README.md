# concourse-resource-bitbucket

This is a fork of https://github.com/Karunamon/concourse-resource-bitbucket. 
This fork is substantially changed from the original.

Summary of changes:

* Targets bitbucket api version 2 instead of 1.
* Only targets bitbucket.org.
* Change auth from user/password to [OAuth client credentials grant](https://developer.atlassian.com/bitbucket/api/2/reference/meta/authentication).
* Support both hg and git repos.
* Create an automated docker build.
* Uses unittests instead of behave for tests.

This repo is tied to the [associated Docker image](https://hub.docker.com/r/ecometrica/concourse-resource-bitbucket/). 
The build of the docker image is using the docker hub automated build. 
The builds will run the tests to make sure that a broken image is never pushed.

## Creating an Access Token
You need to create an OAuth access token for your github team/user account with the following permissions: `Webhooks (r/w), Repositories (r)`

Make sure to **provide a callback URL** (it's not needed at runtime but Bitbucket insists on it anyway). For example, you can use the URL of your concourse instance. Otherwise you will see an error similar to the following
`
Access token result: <Response [400]>{"error_description": "No callback uri defined for the OAuth client.", "error": "invalid_request"}
HTTP 401 Unauthorized - Are your bitbucket credentials correct?
`


## Resource Configuration

These items go in the `source` fields of the resource type. Bold items are required:

 * **`client_id`** - Client id of the OAuth consumer. Shown as `Key` in the bitbucket interface.
 * **`secret`** - Secret for the OAuth consumer.
 * **`repo`** - Full repository name on bitbucket to set build status in. (`<username>/<reponame>`).
 * `debug` - When True, dump the JSON documents sent and received for troubleshooting. (default: false)

## Behavior

### `check`

No-op


### `in`

No-op

### `out`

Update the status of a commit.

Parameters:

 * **`repo`** - Name of the git repo containing the SHA to be updated. 
 This will come from a previous `get` on a `git/hg` resource. 
 Make sure to use the resource directory name, not the name of the resource.
 
 * **`state`** - the state of the status. Must be one of 
 `SUCCESSFUL`, `FAILED`, or `INPROGRESS` - case sensitive.

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

