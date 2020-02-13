About
=====

Update Notifier is a bot written for the Telegram messaging app.
It looks for software updates and informs you about them.

Setup
=====

The configuration file is located in ``data/config.ini``.
You can copy the example configuration from ``data/config-example.ini`` and adapt it to your needs.
Don't forget to change the Telegram API key.

Extensions
==========

You can write extensions to check for updates of you favorite software project.
To do so, write a class that extends ``UpdateChecker`` and implement the ``get_status`` classmethod.
``get_status`` needs to return a tuple containing the current version (e.g. ``1.2.3``), and the download link.
Finally, place your new update checker in the ``update_notifier/checker/checkers`` folder.

Development
===========

The source code is located on `GitHub <https://github.com/eikendev/update_notifier>`_.
To check out the repository, the following command can be used.
::

   git clone https://github.com/eikendev/update_notifier.git
