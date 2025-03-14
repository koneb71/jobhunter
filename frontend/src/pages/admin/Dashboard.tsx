import {
  Users,
  Briefcase,
  Building2,
  TrendingUp,
} from 'lucide-react';

const stats = [
  {
    name: 'Total Users',
    value: '2,543',
    change: '+12.5%',
    changeType: 'increase',
    icon: Users,
  },
  {
    name: 'Active Jobs',
    value: '1,234',
    change: '+8.2%',
    changeType: 'increase',
    icon: Briefcase,
  },
  {
    name: 'Companies',
    value: '456',
    change: '+5.3%',
    changeType: 'increase',
    icon: Building2,
  },
  {
    name: 'Conversion Rate',
    value: '24.57%',
    change: '+2.4%',
    changeType: 'increase',
    icon: TrendingUp,
  },
];

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Overview of your job platform's performance
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <div
            key={stat.name}
            className="relative overflow-hidden rounded-lg bg-white px-4 pt-5 pb-12 shadow sm:px-6 sm:pt-6"
          >
            <dt>
              <div className="absolute rounded-md bg-blue-500 p-3">
                <stat.icon className="h-6 w-6 text-white" aria-hidden="true" />
              </div>
              <p className="ml-16 truncate text-sm font-medium text-gray-500">
                {stat.name}
              </p>
            </dt>
            <dd className="ml-16 flex items-baseline pb-6 sm:pb-7">
              <p className="text-2xl font-semibold text-gray-900">
                {stat.value}
              </p>
              <p
                className={`ml-2 flex items-baseline text-sm font-semibold ${
                  stat.changeType === 'increase'
                    ? 'text-green-600'
                    : 'text-red-600'
                }`}
              >
                {stat.change}
              </p>
            </dd>
          </div>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            Recent Activity
          </h3>
          <div className="mt-5">
            <div className="flow-root">
              <ul role="list" className="-mb-8">
                {[1, 2, 3, 4, 5].map((item, itemIdx) => (
                  <li key={item}>
                    <div className="relative pb-8">
                      {itemIdx !== 4 ? (
                        <span
                          className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                          aria-hidden="true"
                        />
                      ) : null}
                      <div className="relative flex space-x-3">
                        <div>
                          <span className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center ring-8 ring-white">
                            <Users className="h-5 w-5 text-white" />
                          </span>
                        </div>
                        <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                          <div>
                            <p className="text-sm text-gray-500">
                              New user registration{' '}
                              <span className="font-medium text-gray-900">
                                John Doe
                              </span>
                            </p>
                            <p className="text-sm text-gray-500">
                              {new Date().toLocaleDateString()}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 