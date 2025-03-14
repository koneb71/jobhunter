import { useState } from 'react';

interface SettingsForm {
  siteName: string;
  siteDescription: string;
  contactEmail: string;
  enableRegistration: boolean;
  enableJobPosting: boolean;
  enableApplicationTracking: boolean;
}

export default function Settings() {
  const [formData, setFormData] = useState<SettingsForm>({
    siteName: 'JobHunter',
    siteDescription: 'Find your dream job today',
    contactEmail: 'contact@jobhunter.com',
    enableRegistration: true,
    enableJobPosting: true,
    enableApplicationTracking: true,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission
    console.log('Form submitted:', formData);
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value,
    }));
  };

  return (
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Settings</h1>
          <p className="mt-1 text-sm text-gray-500">
            Manage your platform settings and configurations
          </p>
        </div>

        <div className="bg-white shadow rounded-lg">
          <form onSubmit={handleSubmit} className="space-y-6 p-6">
            {/* General Settings */}
            <div>
              <h3 className="text-lg font-medium leading-6 text-gray-900">
                General Settings
              </h3>
              <div className="mt-4 space-y-4">
                <div>
                  <label
                    htmlFor="siteName"
                    className="block text-sm font-medium text-gray-700"
                  >
                    Site Name
                  </label>
                  <input
                    type="text"
                    name="siteName"
                    id="siteName"
                    value={formData.siteName}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label
                    htmlFor="siteDescription"
                    className="block text-sm font-medium text-gray-700"
                  >
                    Site Description
                  </label>
                  <textarea
                    name="siteDescription"
                    id="siteDescription"
                    rows={3}
                    value={formData.siteDescription}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label
                    htmlFor="contactEmail"
                    className="block text-sm font-medium text-gray-700"
                  >
                    Contact Email
                  </label>
                  <input
                    type="email"
                    name="contactEmail"
                    id="contactEmail"
                    value={formData.contactEmail}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                  />
                </div>
              </div>
            </div>

            {/* Feature Settings */}
            <div>
              <h3 className="text-lg font-medium leading-6 text-gray-900">
                Feature Settings
              </h3>
              <div className="mt-4 space-y-4">
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    name="enableRegistration"
                    id="enableRegistration"
                    checked={formData.enableRegistration}
                    onChange={handleChange}
                    className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <label
                    htmlFor="enableRegistration"
                    className="ml-2 block text-sm text-gray-900"
                  >
                    Enable User Registration
                  </label>
                </div>
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    name="enableJobPosting"
                    id="enableJobPosting"
                    checked={formData.enableJobPosting}
                    onChange={handleChange}
                    className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <label
                    htmlFor="enableJobPosting"
                    className="ml-2 block text-sm text-gray-900"
                  >
                    Enable Job Posting
                  </label>
                </div>
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    name="enableApplicationTracking"
                    id="enableApplicationTracking"
                    checked={formData.enableApplicationTracking}
                    onChange={handleChange}
                    className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <label
                    htmlFor="enableApplicationTracking"
                    className="ml-2 block text-sm text-gray-900"
                  >
                    Enable Application Tracking
                  </label>
                </div>
              </div>
            </div>

            <div className="flex justify-end">
              <button
                type="submit"
                className="inline-flex justify-center rounded-md border border-transparent bg-blue-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                Save Changes
              </button>
            </div>
          </form>
        </div>
      </div>
  );
} 