# Playwright

## Before you start

As with Selenium, this assumes you have `poetry` installed. Unlike Selenium, Playwright will attempt to download a browser for you by default if it's not already installed.

## What is Playwright?

Like Selenium, Playwright is an end-to-end testing tool focused on writing tests that interact with a web browser. Playwright was released much more recently (Jan 2020) by Microsoft so is less mature, but does come with a number of additional features which we will explore.

## Try it out

Set up the project with `poetry install`, and then run `poetry run playwright install` to get Playwright to set up the required browsers.

Run `poetry run pytest` to execute the tests. Note that Playwright chooses to default to headless mode, unlike Selenium. Try running them visibly, on Chromium, by adding the `--headed` flag (`poetry run pytest --headed`) or try running them on an alternative browser, e.g. with `--browser firefox`.

## Now it's your turn

A nice feature of Playwright is the ability to generate the code for your tests by interacting with a browser directly. Give that a go, and add a new test exploring [the Playwright demo site](https://demo.playwright.dev/todomvc) by using the `codegen` option:
```
poetry run playwright codegen --target python-pytest demo.playwright.dev/todomvc
```

E.g. create a test that:
* Adds two new to-dos to the list
* Checks both are visible
* Marks one as complete, and deletes the other
* Check only the remaining one is visible

[More guidance on using the Codegen tool is available in the docs.](https://playwright.dev/python/docs/codegen-intro#running-codegen)

If you're interested in seeing the [the list of basic actions you can find that in the Playwright docs.](https://playwright.dev/python/docs/writing-tests#basic-actions)

### Investigate Failures

First, tweak your tests so that they fail, for example in the `test_get_started_link` test you could look for a link with `some text that doesn't exist on the page`.

You should see a timeout error; no link with that text appeared in time, but the stack trace doesn't offer us much more context than that. Was the error a case of the page failing to load anything, or did someone just change a key piece of text?

Investigating end-to-end test issues like this can often be a slow affair, involving running the tests locally in a non-headless mode, slowing them down or introducing breakpoints in order to let us diagnose the problem.

Can we investigate those quicker?

When your tests fail, Playwright offers a number of debug helpful options to speed up your troubleshooting. At this stage, it would be nice to reduce the amount of command line flags we need to pass, so you can add a `pytest.ini` file to your `playwright` directory, with the following content:
```ini
[pytest]
# command line options go here, e.g.:
# addopts = --browser firefox
addopts = 
```

> Note that this assumes you are running the tests from the terminal in the Playwright directory, or that you have opened the playwright subfolder directly in VSCode, otherwise VSCode won't correctly pick up this `pytest.ini` file.

Have a play with the following debugging helpers:
* Capturing a screenshot on failure by setting the `--screenshot` flag to `only-on-failure` (or `on`)
* Capturing a video with the `--video` flag (`on`, or `retain-on-failure`)
* Capturing a "trace with the `--tracing` option (`on` or `retain-on-failure`)
  * This will capture the network activity during the test, so it can be replayed later
  * View these through the Trace Viewer either with the `playwright show-trace <path>` command, or [through the online viewer](https://trace.playwright.dev/)

> Some learners have reported that arguments are only recognised when passed with an `=`, e.g. `--screenshot=on` rather than `--screenshot on`; if the flags seem to be being ignored, then try the alternative syntax.

### Further Reading

- Take a look at [the Playwright best practices](https://playwright.dev/docs/best-practices)
- There's always one more: [Cypress](https://www.cypress.io/) is another popular end-to-end testing tool.
  - Take a look through [Cypress' list of features](https://docs.cypress.io/guides/overview/why-cypress#Features) to get a quick comparison summary.