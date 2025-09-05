using System;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Shapes;
using System.Windows.Threading;
using Newtonsoft.Json;

namespace CursorAutoRegister
{
    public partial class MainWindow : Window
    {
        private Process pythonProcess;
        private bool isRunning = false;
        private DispatcherTimer particleTimer;
        private Random random = new Random();

        public MainWindow()
        {
            InitializeComponent();
            InitializeAnimations();
            CreateParticles();
            LogMessage("Application initialized successfully");
        }

        private void InitializeAnimations()
        {
            // Start particle animation
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

                // Animate particle
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
                var opacity = particle.Opacity;
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

            StartProgressAnimation();
            UpdateStatus("Initializing automation process...");
            LogMessage("Starting registration process");

            try
            {
                await RunPythonAutomation();
            }
            catch (Exception ex)
            {
                LogMessage($"Error: {ex.Message}");
                UpdateStatus("Registration failed");
            }
            finally
            {
                StartButton.IsEnabled = true;
                StopButton.IsEnabled = false;
                isRunning = false;
                StopProgressAnimation();
            }
        }

        private void StopButton_Click(object sender, RoutedEventArgs e)
        {
            if (!isRunning) return;

            try
            {
                pythonProcess?.Kill();
                pythonProcess?.Dispose();
                pythonProcess = null;
            }
            catch (Exception ex)
            {
                LogMessage($"Error stopping process: {ex.Message}");
            }

            StartButton.IsEnabled = true;
            StopButton.IsEnabled = false;
            isRunning = false;
            StopProgressAnimation();
            UpdateStatus("Process stopped by user");
            LogMessage("Registration process stopped");
        }

        private async Task RunPythonAutomation()
        {
            try
            {
                // Create Python script path
                string pythonScript = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "automation_backend.py");
                
                if (!File.Exists(pythonScript))
                {
                    throw new Exception("Python automation script not found");
                }

                // Start Python process
                var startInfo = new ProcessStartInfo
                {
                    FileName = "python",
                    Arguments = $"\"{pythonScript}\"",
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                };

                pythonProcess = new Process { StartInfo = startInfo };
                
                pythonProcess.OutputDataReceived += (sender, e) =>
                {
                    if (!string.IsNullOrEmpty(e.Data))
                    {
                        Dispatcher.Invoke(() =>
                        {
                            try
                            {
                                var message = JsonConvert.DeserializeObject<AutomationMessage>(e.Data);
                                UpdateStatus(message.Status);
                                LogMessage(message.Message);
                            }
                            catch
                            {
                                LogMessage(e.Data);
                            }
                        });
                    }
                };

                pythonProcess.ErrorDataReceived += (sender, e) =>
                {
                    if (!string.IsNullOrEmpty(e.Data))
                    {
                        Dispatcher.Invoke(() => LogMessage($"Error: {e.Data}"));
                    }
                };

                pythonProcess.Start();
                pythonProcess.BeginOutputReadLine();
                pythonProcess.BeginErrorReadLine();

                await Task.Run(() => pythonProcess.WaitForExit());

                if (pythonProcess.ExitCode == 0)
                {
                    UpdateStatus("Registration completed successfully!");
                    LogMessage("✅ Account created successfully!");
                }
                else
                {
                    UpdateStatus("Registration failed");
                    LogMessage("❌ Registration process failed");
                }
            }
            catch (Exception ex)
            {
                UpdateStatus("Error occurred");
                LogMessage($"❌ Error: {ex.Message}");
            }
        }

        private void UpdateStatus(string status)
        {
            Dispatcher.Invoke(() =>
            {
                StatusText.Text = status;
                
                // Add pulse animation to status
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

                pythonProcess?.Kill();
            }

            Application.Current.Shutdown();
        }

        protected override void OnClosed(EventArgs e)
        {
            particleTimer?.Stop();
            pythonProcess?.Kill();
            pythonProcess?.Dispose();
            base.OnClosed(e);
        }
    }

    public class AutomationMessage
    {
        public string Status { get; set; }
        public string Message { get; set; }
    }
}