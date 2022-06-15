// NUnit 3 tests
// See documentation : https://github.com/nunit/docs/wiki/NUnit-Documentation
using System.Collections;
using System.Collections.Generic;
using NUnit.Framework;
using System;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using OpenQA.Selenium;
using OpenQA.Selenium.Firefox;
using OpenQA.Selenium.Support.UI;
namespace NUnit.Selenium
{
    [TestFixture]
    public class TestClass
    {
        private IWebDriver driver;
        private StringBuilder verificationErrors;
        private string baseURL;
        private bool acceptNextAlert = true;

        [SetUp]
        public void SetupTest()
        {
            driver = new FirefoxDriver();
            baseURL = "https://www.google.com/";
            verificationErrors = new StringBuilder();
        }

        [TearDown]
        public void TeardownTest()
        {
            try
            {
                driver.Quit();
            }
            catch (Exception)
            {
                // Ignore errors if unable to close the browser
            }
            Assert.AreEqual("", verificationErrors.ToString());
        }

        [Test]
        public void TheUntitledTestCaseTest()
        {
            driver.Navigate().GoToUrl("https://elp.duetbd.org/login/index.php");
            driver.FindElement(By.Id("username")).Clear();
            driver.FindElement(By.Id("username")).SendKeys("170042017");
            driver.FindElement(By.Id("password")).Clear();
            driver.FindElement(By.Id("password")).SendKeys("Abc.1234");
            driver.FindElement(By.XPath("//section[@id='region-main']/div/div[2]")).Click();
            driver.FindElement(By.Id("password")).Click();
            driver.FindElement(By.Id("password")).Click();
            driver.FindElement(By.Id("password")).Click();
            driver.FindElement(By.Id("loginbtn")).Click();
            driver.FindElement(By.XPath("//img[contains(@src,'https://elp.duetbd.org/pluginfile.php/46142/user/icon/academi/f2?rev=113245')]")).Click();
            driver.FindElement(By.Id("actionmenuaction-6")).Click();
            driver.FindElement(By.Id("login_username")).Clear();
            driver.FindElement(By.Id("login_username")).SendKeys("170042017");
            driver.FindElement(By.Id("login_password")).Clear();
            driver.FindElement(By.Id("login_password")).SendKeys("Abc.1234");
        }
        private bool IsElementPresent(By by)
        {
            try
            {
                driver.FindElement(by);
                return true;
            }
            catch (NoSuchElementException)
            {
                return false;
            }
        }

        private bool IsAlertPresent()
        {
            try
            {
                driver.SwitchTo().Alert();
                return true;
            }
            catch (NoAlertPresentException)
            {
                return false;
            }
        }

        private string CloseAlertAndGetItsText()
        {
            try
            {
                IAlert alert = driver.SwitchTo().Alert();
                string alertText = alert.Text;
                if (acceptNextAlert)
                {
                    alert.Accept();
                }
                else
                {
                    alert.Dismiss();
                }
                return alertText;
            }
            finally
            {
                acceptNextAlert = true;
            }
        }
    }


}
