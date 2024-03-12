# Selenium

## Before you start

This assumes you have:
- Poetry installed on your machine
  - If not, install it [according to the instructions here](https://python-poetry.org/docs/#installation). 
- Chrome installed
  - The test can easily be adjusted for FireFox or Safari if you prefer those.

## What is Selenium?

[Selenium](https://www.selenium.dev/) is a popular open-source UI testing library. It creates language-specific bindings for programmatically controlling a web browser so you can write tests in almost any mainstream programming language, including Python. Let’s look at how you can use Selenium, with Python, to automate UI interactions.

To run Selenium, you'll need a web driver for a browser that you have installed locally. Recent versions of Selenium should install that for you when it runs, but you can find web drivers to download yourself listed [in the selenium docs](https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/driver_location/#download-the-driver). 

## Try it out

Set up the project with `poetry install` from the `e2e-selenium` folder.

You should then be able to run the existing test with `poetry run pytest` - check that you can see a browser appear and navigate Google without input!

> If you aren't using Chrome, take a look at the `.env` file and adjust the variable to run the browser of your choice.

## Now it's your turn

### Extend the steps
Have a look over the Selenium code written in `tests/example_test.py`. You can then have a go at using Selenium to navigate Selenium's own website!

Update the test to instead visit [https://www.selenium.dev/](https://www.selenium.dev/) and navigate - can you switch to the "Documentation" tab, and then successfully manipulate the search box & click on the first suggested link?

You may want to look at the docs for:
* [Locating by Class](https://selenium-python.readthedocs.io/locating-elements.html#locating-elements-by-class-name)
* [Locating by XPath](https://selenium-python.readthedocs.io/locating-elements.html#locating-by-xpath)
* [Locating by Link Text](https://selenium-python.readthedocs.io/locating-elements.html#locating-hyperlinks-by-link-text)

If you see problems with Selenium expecting things before the page is ready, then read the section [on Waiting](#on-waiting) below.

> Selenium can be a little slow to fire up, so your feedback loop for testing different code can easily crawl! A good pattern is to add an appropriate breakpoint and run your test in debugging mode, so you can take advantage of the Debug Console for quick experimentation of different code.

### On Waiting

When you interact with a webpage, its response isn't instantaneous. Sometimes Selenium will attempt to complete an action before the page is ready, causing it to fail. For example, if you imagine typing some words in Google's search box and then trying to hit the first auto-complete suggestion, before the browser has managed to render the options.

Sometimes we need to advise our testing code to be aware of this and whilst often the easiest approach is simply to tell our test to sleep, it is a bad habit! Enforcing sleeps is a great way to make our testing loop arbitrarily slower, whilst missing the underlying cause and therefore still often triggering flaky behaviour.

 Selenium offers two approaches to waiting:

**Implicit Waits** are where we tell Selenium a standard rule of how long to look for things. The default is 0, so Selenium will immediately fail if an element isn't found, but when overridden is set for the lifetime of the WebDriver.
```python
# Poll the webpage for *up to* 10 seconds when looking for 
# elements that aren't immediately available
driver.implicitly_wait(10)
```

**Explicit Waits** are a tool for specifying explicitly what to wait for before proceeding to the next step. For example the code below waits until the `slowLoadingElement` is found on [the DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction).
```python
element = WebDriverWait(driver, 10).until(
    expected_conditions.presence_of_element_located((By.ID, "slowLoadingElement"))
)
```

[If you're interested, Selenium has more info on waiting here.](https://selenium-python.readthedocs.io/waits.html)

### Save an output screenshot

Debugging Selenium tests can get fiddly, particularly with the pace at which the browser often navigates. Try saving a screenshot with the `driver.save_screenshot(<filename>)` function at different stages of your test.

### Speed it up

Now that it's working, try switching your driver into "headless mode" - this runs without the browser UI appearing, and is a common requirement for environments that lack a display (e.g. allowing you to run these tests within a container).

<details> <summary>Hint</summary> 

```python
  opt = webdriver.ChromeOptions()
  opt.add_argument("--headless=new")
```
</details>

### Test your own sites

Add a new test file in the `tests` folder, and point your test at another website, for example one that you work on or with. Can you get the test to navigate through a simple real user journey?

> If you don't have an appropriate website to trial, we'll shortly use [the Playwright demo site](https://demo.playwright.dev/todomvc) to test Playwright, so you can use that to get a comparison.

> Alternatively, have a go at adding useful end-to-end tests to the [Chessington testing exercise](https://github.com/corndeladmin/Devops-Chessington-Python) - can you get Selenium to play out a game of chess?

### Further reading

- [Selenium's documentation](https://www.selenium.dev/documentation/)
- [Selenium Pytest integration plugin](https://pytest-selenium.readthedocs.io/en/latest/user_guide.html)
  - Adds a number of useful features to simplify management of large Selenium repositories