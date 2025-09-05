using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Shapes;
using System.Windows.Threading;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Support.UI;
using WebDriverManager;
using WebDriverManager.DriverConfigs.Impl;

namespace CursorAutoRegister
{
    public partial class MainWindow : Window
    {
        private IWebDriver driver;
        private bool isRunning = false;
        private DispatcherTimer particleTimer;
        private Random random = new Random();
        private CancellationTokenSource cancellationTokenSource;
        private string tempEmail = "";
        private string password = "";

        public MainWindow()
        {
            InitializeComponent();
            InitializeAnimations();
            CreateParticles();
            LogMessage("🚀 Application initialized successfully");
        }

        private void InitializeAnimations()
        {
            particleTimer = new DispatcherTimer();
            particleTimer.Interval = TimeSpan.FromMilliseconds(100);
            particleTimer.Tick += UpdateParticles;
            particleTimer.Start();
        }

        private void CreateParticles()
        {
            for (int i = 0; i < 50; i++)
            {
                var particle = new Ellipse
                {
                    Width = random.Next(2, 6),
                    Height = random.Next(2, 6),
                    Fill = new SolidColorBrush(Color.FromArgb(
                        (byte)random.Next(50, 150),
                        (byte)random.Next(168, 255),
                        85,
                        247))
                };

                Canvas.SetLeft(particle, random.Next(0, 1000));
                Canvas.SetTop(particle, random.Next(0, 800));
                
                ParticleCanvas.Children.Add(particle);

                var storyboard = new Storyboard();
                var animationX = new DoubleAnimation
                {
                    From = Canvas.GetLeft(particle),
                    To = Canvas.GetLeft(particle) + random.Next(-100, 100),
                    Duration = TimeSpan.FromSeconds(random.Next(3, 8)),
                    RepeatBehavior = RepeatBehavior.Forever,
                    AutoReverse = true
                };

                var animationY = new DoubleAnimation
                {
                    From = Canvas.GetTop(particle),
                    To = Canvas.GetTop(particle) + random.Next(-50, 50),
                    Duration = TimeSpan.FromSeconds(random.Next(4, 10)),
                    RepeatBehavior = RepeatBehavior.Forever,
                    AutoReverse = true
                };

                Storyboard.SetTarget(animationX, particle);
                Storyboard.SetTargetProperty(animationX, new PropertyPath("(Canvas.Left)"));
                Storyboard.SetTarget(animationY, particle);
                Storyboard.SetTargetProperty(animationY, new PropertyPath("(Canvas.Top)"));

                storyboard.Children.Add(animationX);
                storyboard.Children.Add(animationY);
                storyboard.Begin();
            }
        }

        private void UpdateParticles(object sender, EventArgs e)
        {
            foreach (Ellipse particle in ParticleCanvas.Children)
            {
                particle.Opacity = 0.3 + (Math.Sin(DateTime.Now.Millisecond * 0.01) + 1) * 0.2;
            }
        }

        private void StartProgressAnimation()
        {
            var storyboard = (Storyboard)FindResource("ProgressAnimation");
            Storyboard.SetTarget(storyboard, ProgressBar);
            storyboard.Begin();
        }

        private void StopProgressAnimation()
        {
            var storyboard = (Storyboard)FindResource("ProgressAnimation");
            storyboard.Stop();
            ProgressBar.SetValue(Canvas.LeftProperty, -100.0);
        }

        private async void StartButton_Click(object sender, RoutedEventArgs e)
        {
            if (isRunning) return;

            StartButton.IsEnabled = false;
            StopButton.IsEnabled = true;
            isRunning = true;
            cancellationTokenSource = new CancellationTokenSource();

            StartProgressAnimation();
            UpdateStatus("🚀 Initializing automation process...");
            LogMessage("Starting registration process");

            try
            {
                await RunAutomation(cancellationTokenSource.Token);
            }
            catch (OperationCanceledException)
            {
                LogMessage("⏹️ Registration process cancelled");
                UpdateStatus("Process stopped by user");
            }
            catch (Exception ex)
            {
                LogMessage($"❌ Error: {ex.Message}");
                UpdateStatus("Registration failed");
            }
            finally
            {
                StartButton.IsEnabled = true;
                StopButton.IsEnabled = false;
                isRunning = false;
                StopProgressAnimation();
                driver?.Quit();
                driver?.Dispose();
            }
        }

        private void StopButton_Click(object sender, RoutedEventArgs e)
        {
            if (!isRunning) return;

            cancellationTokenSource?.Cancel();
            driver?.Quit();
            
            StartButton.IsEnabled = true;
            StopButton.IsEnabled = false;
            isRunning = false;
            StopProgressAnimation();
            UpdateStatus("⏹️ Process stopped by user");
            LogMessage("Registration process stopped");
        }

        private async Task RunAutomation(CancellationToken cancellationToken)
        {
            try
            {
                UpdateStatus("🌐 Starting Chrome browser...");
                LogMessage("Initializing Chrome browser in incognito mode");

                var driverPath = new DriverManager().SetUpDriver(new ChromeConfig());
                var options = new ChromeOptions();
                options.AddArgument("--incognito");
                options.AddArgument("--disable-blink-features=AutomationControlled");
                options.AddExcludedArgument("enable-automation");
                options.AddAdditionalOption("useAutomationExtension", false);
                options.AddArgument("--disable-gpu");
                options.AddArgument("--no-sandbox");

                var service = ChromeDriverService.CreateDefaultService(System.IO.Path.GetDirectoryName(driverPath));
                driver = new ChromeDriver(service, options);
                ((IJavaScriptExecutor)driver).ExecuteScript("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})");

                cancellationToken.ThrowIfCancellationRequested();

                UpdateStatus("🌐 Navigating to Cursor sign-up...");
                LogMessage("Opening Cursor registration page");
                driver.Navigate().GoToUrl("https://authenticator.cursor.sh/sign-up");

                await Task.Delay(3000, cancellationToken);

                var (firstName, lastName) = GenerateRandomName();
                UpdateStatus("👤 Generated user details");
                LogMessage($"Generated name: {firstName} {lastName}");

                tempEmail = await GetTempEmail(cancellationToken);
                if (string.IsNullOrEmpty(tempEmail))
                    throw new Exception("Failed to get temporary email");

                UpdateStatus("📝 Filling registration form...");
                LogMessage("Entering user information");

                var wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
                
                var firstNameField = wait.Until(d => d.FindElement(By.Name("firstName")));
                firstNameField.SendKeys(firstName);
                await Task.Delay(1000, cancellationToken);

                var lastNameField = driver.FindElement(By.Name("lastName"));
                lastNameField.SendKeys(lastName);
                await Task.Delay(1000, cancellationToken);

                var emailField = driver.FindElement(By.Name("email"));
                emailField.SendKeys(tempEmail);
                await Task.Delay(1000, cancellationToken);

                var continueButton = driver.FindElement(By.XPath("//button[contains(text(), 'Continue')]"));
                continueButton.Click();

                await Task.Delay(3000, cancellationToken);

                UpdateStatus("🔐 Setting password...");
                LogMessage("Creating secure password");

                password = GeneratePassword();
                LogMessage($"Generated password: {password}");

                var passwordField = wait.Until(d => d.FindElement(By.Name("password")));
                passwordField.SendKeys(password);
                await Task.Delay(1000, cancellationToken);

                continueButton = driver.FindElement(By.XPath("//button[contains(text(), 'Continue')]"));
                continueButton.Click();

                await Task.Delay(3000, cancellationToken);

                var verificationCode = await GetVerificationCode(cancellationToken);
                if (string.IsNullOrEmpty(verificationCode))
                    throw new Exception("Failed to get verification code");

                UpdateStatus("✅ Entering verification code...");
                LogMessage("Completing verification");

                var codeField = wait.Until(d => d.FindElement(By.Name("code")));
                codeField.SendKeys(verificationCode);
                await Task.Delay(1000, cancellationToken);

                var verifyButton = driver.FindElement(By.XPath("//button[contains(text(), 'Verify')]"));
                verifyButton.Click();

                await Task.Delay(5000, cancellationToken);

                UpdateStatus("🎉 Registration completed successfully!");
                LogMessage("✅ Account created successfully!");
                LogMessage($"📋 Name: {firstName} {lastName}");
                LogMessage($"📧 Email: {tempEmail}");
                LogMessage($"🔑 Password: {password}");

                MessageBox.Show("Cursor account registered successfully!", "Success", 
                    MessageBoxButton.OK, MessageBoxImage.Information);
            }
            catch (OperationCanceledException)
            {
                throw;
            }
            catch (Exception ex)
            {
                UpdateStatus("❌ Registration failed");
                LogMessage($"Error: {ex.Message}");
                throw;
            }
        }

        private (string, string) GenerateRandomName()
        {
            var firstNames = new[] { "Alex", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Avery", "Quinn", 
                "Blake", "Cameron", "Drew", "Emery", "Finley", "Harper", "Hayden", "Jamie",
                "Kendall", "Logan", "Parker", "Peyton", "Reese", "River", "Rowan", "Sage",
                "Skyler", "Sydney", "Tanner", "Teagan", "Tyler", "Winter" };
            
            var lastNames = new[] { "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
                "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
                "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
                "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson" };
            
            return (firstNames[random.Next(firstNames.Length)], lastNames[random.Next(lastNames.Length)]);
        }

        private string GeneratePassword()
        {
            var passwords = new[] { "sunshine123", "password123", "welcome123", "hello123", "computer123",
                "internet123", "freedom123", "rainbow123", "butterfly123", "mountain123" };
            return passwords[random.Next(passwords.Length)];
        }

        private async Task<string> GetTempEmail(CancellationToken cancellationToken)
        {
            try
            {
                UpdateStatus("📧 Getting temporary email...");
                LogMessage("Connecting to temp-mail.org");

                var options = new ChromeOptions();
                options.AddArgument("--headless");
                options.AddArgument("--no-sandbox");
                options.AddArgument("--disable-dev-shm-usage");
                options.AddArgument("--disable-gpu");

                var driverPath = new DriverManager().SetUpDriver(new ChromeConfig());
                var service = ChromeDriverService.CreateDefaultService(System.IO.Path.GetDirectoryName(driverPath));
                using var tempDriver = new ChromeDriver(service, options);
                
                tempDriver.Navigate().GoToUrl("https://temp-mail.org/en/");
                await Task.Delay(3000, cancellationToken);

                var emailElement = tempDriver.FindElement(By.Id("mail"));
                var email = emailElement.GetAttribute("value");

                if (!string.IsNullOrEmpty(email))
                {
                    LogMessage($"���� Email obtained: {email}");
                    return email;
                }
                
                throw new Exception("Could not get temporary email");
            }
            catch (Exception ex)
            {
                LogMessage($"❌ Error getting email: {ex.Message}");
                return null;
            }
        }

        private async Task<string> GetVerificationCode(CancellationToken cancellationToken)
        {
            try
            {
                UpdateStatus("📬 Checking for verification email...");
                LogMessage("Waiting for verification code");

                var options = new ChromeOptions();
                options.AddArgument("--headless");
                options.AddArgument("--no-sandbox");
                options.AddArgument("--disable-dev-shm-usage");
                options.AddArgument("--disable-gpu");

                var driverPath = new DriverManager().SetUpDriver(new ChromeConfig());
                var service = ChromeDriverService.CreateDefaultService(System.IO.Path.GetDirectoryName(driverPath));
                using var tempDriver = new ChromeDriver(service, options);
                
                tempDriver.Navigate().GoToUrl("https://temp-mail.org/en/");
                await Task.Delay(2000, cancellationToken);

                var emailInput = tempDriver.FindElement(By.Id("mail"));
                emailInput.Clear();
                emailInput.SendKeys(tempEmail);
                emailInput.SendKeys(Keys.Enter);

                await Task.Delay(3000, cancellationToken);

                for (int attempt = 0; attempt < 30; attempt++)
                {
                    cancellationToken.ThrowIfCancellationRequested();

                    try
                    {
                        var refreshButton = tempDriver.FindElement(By.ClassName("refresh"));
                        refreshButton.Click();
                        await Task.Delay(2000, cancellationToken);

                        var emails = tempDriver.FindElements(By.ClassName("mail"));
                        
                        foreach (var email in emails)
                        {
                            if (email.Text.Contains("Cursor") || email.Text.ToLower().Contains("verify"))
                            {
                                email.Click();
                                await Task.Delay(2000, cancellationToken);

                                var emailContent = tempDriver.FindElement(By.ClassName("mail-content"));
                                var contentText = emailContent.Text;

                                var codeMatch = Regex.Match(contentText, @"\b\d{6}\b");
                                if (codeMatch.Success)
                                {
                                    var verificationCode = codeMatch.Value;
                                    LogMessage($"🔑 Verification code found: {verificationCode}");
                                    return verificationCode;
                                }
                            }
                        }

                        LogMessage($"⏳ Waiting for email... (attempt {attempt + 1}/30)");
                        await Task.Delay(5000, cancellationToken);
                    }
                    catch (Exception)
                    {
                        await Task.Delay(2000, cancellationToken);
                        continue;
                    }
                }

                return null;
            }
            catch (Exception ex)
            {
                LogMessage($"❌ Error getting verification code: {ex.Message}");
                return null;
            }
        }

        private void UpdateStatus(string status)
        {
            Dispatcher.Invoke(() =>
            {
                StatusText.Text = status;
                
                var storyboard = (Storyboard)FindResource("PulseAnimation");
                Storyboard.SetTarget(storyboard, StatusText);
                storyboard.Begin();
            });
        }

        private void LogMessage(string message)
        {
            Dispatcher.Invoke(() =>
            {
                string timestamp = DateTime.Now.ToString("HH:mm:ss");
                string logEntry = $"[{timestamp}] {message}\n";
                
                LogText.Text += logEntry;
                LogScrollViewer.ScrollToEnd();
            });
        }

        private void CloseButton_Click(object sender, RoutedEventArgs e)
        {
            if (isRunning)
            {
                var result = MessageBox.Show(
                    "Registration is in progress. Are you sure you want to exit?",
                    "Confirm Exit",
                    MessageBoxButton.YesNo,
                    MessageBoxImage.Question);

                if (result == MessageBoxResult.No)
                    return;

                cancellationTokenSource?.Cancel();
                driver?.Quit();
            }

            Application.Current.Shutdown();
        }

        protected override void OnClosed(EventArgs e)
        {
            particleTimer?.Stop();
            cancellationTokenSource?.Cancel();
            driver?.Quit();
            driver?.Dispose();
            base.OnClosed(e);
        }
    }
}