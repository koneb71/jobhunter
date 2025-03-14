import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  User,
  Bell,
  Lock,
  Globe,
  Mail,
  Eye,
  EyeOff,
  Trash2,
  Save,
  X,
} from 'lucide-react';
import { toast } from 'react-hot-toast';

interface SettingsData {
  account: {
    full_name: string;
    email: string;
    phone: string;
    current_password: string;
    new_password: string;
    confirm_password: string;
  };
  notifications: {
    email_notifications: boolean;
    push_notifications: boolean;
    job_alerts: boolean;
    application_updates: boolean;
    marketing_emails: boolean;
  };
  privacy: {
    profile_visibility: 'public' | 'private' | 'connections';
    show_email: boolean;
    show_phone: boolean;
    show_location: boolean;
  };
  preferences: {
    language: string;
    timezone: string;
    theme: 'light' | 'dark' | 'system';
    job_alerts_frequency: 'daily' | 'weekly' | 'monthly';
  };
}

const Settings: React.FC = () => {
  const [activeTab, setActiveTab] = useState('account');
  const [showPassword, setShowPassword] = useState(false);
  const [settings, setSettings] = useState<SettingsData>({
    account: {
      full_name: 'John Doe',
      email: 'john@example.com',
      phone: '+1 234 567 8900',
      current_password: '',
      new_password: '',
      confirm_password: '',
    },
    notifications: {
      email_notifications: true,
      push_notifications: true,
      job_alerts: true,
      application_updates: true,
      marketing_emails: false,
    },
    privacy: {
      profile_visibility: 'public',
      show_email: true,
      show_phone: false,
      show_location: true,
    },
    preferences: {
      language: 'en',
      timezone: 'UTC',
      theme: 'system',
      job_alerts_frequency: 'daily',
    },
  });

  const handleInputChange = (
    section: keyof SettingsData,
    field: string,
    value: string | boolean
  ) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value,
      },
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/settings', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings),
      });

      if (!response.ok) throw new Error('Failed to update settings');

      toast.success('Settings updated successfully');
    } catch (error) {
      toast.error('Failed to update settings');
      console.error('Error updating settings:', error);
    }
  };

  const tabs = [
    { id: 'account', label: 'Account', icon: User },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'privacy', label: 'Privacy', icon: Lock },
    { id: 'preferences', label: 'Preferences', icon: Globe },
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="bg-white rounded-lg shadow">
          <div className="px-4 py-5 sm:p-6">
            <h1 className="text-2xl font-bold text-gray-900 mb-8">Settings</h1>

            <div className="flex space-x-8 border-b border-gray-200">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center px-1 py-4 border-b-2 font-medium text-sm ${
                      activeTab === tab.id
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <Icon className="h-5 w-5 mr-2" />
                    {tab.label}
                  </button>
                );
              })}
            </div>

            <form onSubmit={handleSubmit} className="mt-8">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
              >
                {activeTab === 'account' && (
                  <div className="space-y-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Full Name
                      </label>
                      <input
                        type="text"
                        value={settings.account.full_name}
                        onChange={(e) =>
                          handleInputChange('account', 'full_name', e.target.value)
                        }
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Email
                      </label>
                      <input
                        type="email"
                        value={settings.account.email}
                        onChange={(e) =>
                          handleInputChange('account', 'email', e.target.value)
                        }
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Phone
                      </label>
                      <input
                        type="tel"
                        value={settings.account.phone}
                        onChange={(e) =>
                          handleInputChange('account', 'phone', e.target.value)
                        }
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Current Password
                      </label>
                      <div className="mt-1 relative">
                        <input
                          type={showPassword ? 'text' : 'password'}
                          value={settings.account.current_password}
                          onChange={(e) =>
                            handleInputChange(
                              'account',
                              'current_password',
                              e.target.value
                            )
                          }
                          className="block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                        />
                        <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute inset-y-0 right-0 pr-3 flex items-center"
                        >
                          {showPassword ? (
                            <EyeOff className="h-5 w-5 text-gray-400" />
                          ) : (
                            <Eye className="h-5 w-5 text-gray-400" />
                          )}
                        </button>
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        New Password
                      </label>
                      <input
                        type="password"
                        value={settings.account.new_password}
                        onChange={(e) =>
                          handleInputChange('account', 'new_password', e.target.value)
                        }
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Confirm New Password
                      </label>
                      <input
                        type="password"
                        value={settings.account.confirm_password}
                        onChange={(e) =>
                          handleInputChange(
                            'account',
                            'confirm_password',
                            e.target.value
                          )
                        }
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                      />
                    </div>
                  </div>
                )}

                {activeTab === 'notifications' && (
                  <div className="space-y-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-sm font-medium text-gray-900">
                          Email Notifications
                        </h3>
                        <p className="text-sm text-gray-500">
                          Receive notifications via email
                        </p>
                      </div>
                      <button
                        type="button"
                        onClick={() =>
                          handleInputChange(
                            'notifications',
                            'email_notifications',
                            !settings.notifications.email_notifications
                          )
                        }
                        className={`${
                          settings.notifications.email_notifications
                            ? 'bg-blue-600'
                            : 'bg-gray-200'
                        } relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2`}
                      >
                        <span
                          className={`${
                            settings.notifications.email_notifications
                              ? 'translate-x-5'
                              : 'translate-x-0'
                          } pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out`}
                        />
                      </button>
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-sm font-medium text-gray-900">
                          Push Notifications
                        </h3>
                        <p className="text-sm text-gray-500">
                          Receive push notifications in your browser
                        </p>
                      </div>
                      <button
                        type="button"
                        onClick={() =>
                          handleInputChange(
                            'notifications',
                            'push_notifications',
                            !settings.notifications.push_notifications
                          )
                        }
                        className={`${
                          settings.notifications.push_notifications
                            ? 'bg-blue-600'
                            : 'bg-gray-200'
                        } relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2`}
                      >
                        <span
                          className={`${
                            settings.notifications.push_notifications
                              ? 'translate-x-5'
                              : 'translate-x-0'
                          } pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out`}
                        />
                      </button>
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-sm font-medium text-gray-900">
                          Job Alerts
                        </h3>
                        <p className="text-sm text-gray-500">
                          Receive alerts for new job matches
                        </p>
                      </div>
                      <button
                        type="button"
                        onClick={() =>
                          handleInputChange(
                            'notifications',
                            'job_alerts',
                            !settings.notifications.job_alerts
                          )
                        }
                        className={`${
                          settings.notifications.job_alerts
                            ? 'bg-blue-600'
                            : 'bg-gray-200'
                        } relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2`}
                      >
                        <span
                          className={`${
                            settings.notifications.job_alerts
                              ? 'translate-x-5'
                              : 'translate-x-0'
                          } pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out`}
                        />
                      </button>
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-sm font-medium text-gray-900">
                          Application Updates
                        </h3>
                        <p className="text-sm text-gray-500">
                          Receive updates about your job applications
                        </p>
                      </div>
                      <button
                        type="button"
                        onClick={() =>
                          handleInputChange(
                            'notifications',
                            'application_updates',
                            !settings.notifications.application_updates
                          )
                        }
                        className={`${
                          settings.notifications.application_updates
                            ? 'bg-blue-600'
                            : 'bg-gray-200'
                        } relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2`}
                      >
                        <span
                          className={`${
                            settings.notifications.application_updates
                              ? 'translate-x-5'
                              : 'translate-x-0'
                          } pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out`}
                        />
                      </button>
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-sm font-medium text-gray-900">
                          Marketing Emails
                        </h3>
                        <p className="text-sm text-gray-500">
                          Receive emails about new features and promotions
                        </p>
                      </div>
                      <button
                        type="button"
                        onClick={() =>
                          handleInputChange(
                            'notifications',
                            'marketing_emails',
                            !settings.notifications.marketing_emails
                          )
                        }
                        className={`${
                          settings.notifications.marketing_emails
                            ? 'bg-blue-600'
                            : 'bg-gray-200'
                        } relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2`}
                      >
                        <span
                          className={`${
                            settings.notifications.marketing_emails
                              ? 'translate-x-5'
                              : 'translate-x-0'
                          } pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out`}
                        />
                      </button>
                    </div>
                  </div>
                )}

                {activeTab === 'privacy' && (
                  <div className="space-y-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Profile Visibility
                      </label>
                      <select
                        value={settings.privacy.profile_visibility}
                        onChange={(e) =>
                          handleInputChange(
                            'privacy',
                            'profile_visibility',
                            e.target.value
                          )
                        }
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                      >
                        <option value="public">Public</option>
                        <option value="private">Private</option>
                        <option value="connections">Connections Only</option>
                      </select>
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-sm font-medium text-gray-900">
                          Show Email
                        </h3>
                        <p className="text-sm text-gray-500">
                          Allow others to see your email address
                        </p>
                      </div>
                      <button
                        type="button"
                        onClick={() =>
                          handleInputChange(
                            'privacy',
                            'show_email',
                            !settings.privacy.show_email
                          )
                        }
                        className={`${
                          settings.privacy.show_email
                            ? 'bg-blue-600'
                            : 'bg-gray-200'
                        } relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2`}
                      >
                        <span
                          className={`${
                            settings.privacy.show_email
                              ? 'translate-x-5'
                              : 'translate-x-0'
                          } pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out`}
                        />
                      </button>
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-sm font-medium text-gray-900">
                          Show Phone
                        </h3>
                        <p className="text-sm text-gray-500">
                          Allow others to see your phone number
                        </p>
                      </div>
                      <button
                        type="button"
                        onClick={() =>
                          handleInputChange(
                            'privacy',
                            'show_phone',
                            !settings.privacy.show_phone
                          )
                        }
                        className={`${
                          settings.privacy.show_phone
                            ? 'bg-blue-600'
                            : 'bg-gray-200'
                        } relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2`}
                      >
                        <span
                          className={`${
                            settings.privacy.show_phone
                              ? 'translate-x-5'
                              : 'translate-x-0'
                          } pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out`}
                        />
                      </button>
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-sm font-medium text-gray-900">
                          Show Location
                        </h3>
                        <p className="text-sm text-gray-500">
                          Allow others to see your location
                        </p>
                      </div>
                      <button
                        type="button"
                        onClick={() =>
                          handleInputChange(
                            'privacy',
                            'show_location',
                            !settings.privacy.show_location
                          )
                        }
                        className={`${
                          settings.privacy.show_location
                            ? 'bg-blue-600'
                            : 'bg-gray-200'
                        } relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2`}
                      >
                        <span
                          className={`${
                            settings.privacy.show_location
                              ? 'translate-x-5'
                              : 'translate-x-0'
                          } pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out`}
                        />
                      </button>
                    </div>
                  </div>
                )}

                {activeTab === 'preferences' && (
                  <div className="space-y-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Language
                      </label>
                      <select
                        value={settings.preferences.language}
                        onChange={(e) =>
                          handleInputChange('preferences', 'language', e.target.value)
                        }
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                      >
                        <option value="en">English</option>
                        <option value="es">Spanish</option>
                        <option value="fr">French</option>
                        <option value="de">German</option>
                        <option value="it">Italian</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Timezone
                      </label>
                      <select
                        value={settings.preferences.timezone}
                        onChange={(e) =>
                          handleInputChange('preferences', 'timezone', e.target.value)
                        }
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                      >
                        <option value="UTC">UTC</option>
                        <option value="EST">Eastern Time</option>
                        <option value="CST">Central Time</option>
                        <option value="MST">Mountain Time</option>
                        <option value="PST">Pacific Time</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Theme
                      </label>
                      <select
                        value={settings.preferences.theme}
                        onChange={(e) =>
                          handleInputChange('preferences', 'theme', e.target.value)
                        }
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                      >
                        <option value="light">Light</option>
                        <option value="dark">Dark</option>
                        <option value="system">System</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Job Alerts Frequency
                      </label>
                      <select
                        value={settings.preferences.job_alerts_frequency}
                        onChange={(e) =>
                          handleInputChange(
                            'preferences',
                            'job_alerts_frequency',
                            e.target.value
                          )
                        }
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                      >
                        <option value="daily">Daily</option>
                        <option value="weekly">Weekly</option>
                        <option value="monthly">Monthly</option>
                      </select>
                    </div>
                  </div>
                )}
              </motion.div>

              <div className="mt-8 flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => {
                    // Reset form to initial values
                    setSettings({
                      account: {
                        full_name: 'John Doe',
                        email: 'john@example.com',
                        phone: '+1 234 567 8900',
                        current_password: '',
                        new_password: '',
                        confirm_password: '',
                      },
                      notifications: {
                        email_notifications: true,
                        push_notifications: true,
                        job_alerts: true,
                        application_updates: true,
                        marketing_emails: false,
                      },
                      privacy: {
                        profile_visibility: 'public',
                        show_email: true,
                        show_phone: false,
                        show_location: true,
                      },
                      preferences: {
                        language: 'en',
                        timezone: 'UTC',
                        theme: 'system',
                        job_alerts_frequency: 'daily',
                      },
                    });
                  }}
                  className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  <X className="h-5 w-5 mr-2" />
                  Reset
                </button>
                <button
                  type="submit"
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  <Save className="h-5 w-5 mr-2" />
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings; 