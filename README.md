Vimeo XBlock
============

This XBlock allows course creators to stream videos from [Vimeo](https://vimeo.com/) from within their courses.

Support
-------
| Open edX Release | Tag |
|:-----------------|:---:|
| Juniper | v0.5 |
| Ironwood | v0.5 |

> ###### Tested on Python 3.5, 3.8. Manually tested on Python 2.7.

Install
-------

See [edX Installing an XBlock](http://edx.readthedocs.io/projects/edx-installing-configuring-and-running/en/latest/configuration/install_xblock.html?highlight=install%20xblock)
for details on how to install this XBlock on your Open edX instance.

```python
pip install "git+https://github.com/open-craft/xblock-vimeo@master#egg=xblock-vimeo"
```

Usage
-----

To enable the `vimeo` xblock in your course:

1. In Studio, go to `Settings > Advanced Settings`.
2. Locate the `Advanced Module List` field, and add `"vimeo"` to that list.
3. Add a Unit to your course, and click on the `Advanced` button to add a `Vimeo` component.
4. Click `Edit` to add your Video URL, located on [vimeo.com](https://vimeo.com).
5. Click Save to add the video to your course.

Testing
-----

1. Make sure you have `tox` installed.
2. Run the tox tests using the `tox` command.

Installing on DevStack
-----

1. Start your *edX devstack*
2. Once the *edX devstack* is up, run `make studio-shell`
3. `source ../venvs/edxapp/bin/activate`
4. `sudo -u edxapp /edx/bin/pip.edxapp install "git+https://github.com/open-craft/xblock-vimeo@nizar/juniper_upgrade#egg=xblock-vimeo"`
5. `docker-compose restart studio`
6. Repeat steps 2 till 5 using `lms` instead of `studio`, ei `make lms-shell` and `docker-compose restart lms`.