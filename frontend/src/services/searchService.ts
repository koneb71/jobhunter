import { JobSearchParams } from './jobService';

const SEARCH_HISTORY_KEY = 'job_search_history';
const MAX_HISTORY_ITEMS = 10;

export interface SearchHistoryItem {
  params: JobSearchParams;
  timestamp: number;
}

export interface JobSuggestion {
  id: string;
  title: string;
  company: string;
  match_score: number;
  reason: string;
}

const searchService = {
  // Search History
  getSearchHistory(): SearchHistoryItem[] {
    try {
      const history = localStorage.getItem(SEARCH_HISTORY_KEY);
      return history ? JSON.parse(history) : [];
    } catch (error) {
      console.error('Error reading search history:', error);
      return [];
    }
  },

  addToSearchHistory(params: JobSearchParams): void {
    try {
      const history = this.getSearchHistory();
      const newItem: SearchHistoryItem = {
        params,
        timestamp: Date.now()
      };

      // Remove duplicate searches
      const filteredHistory = history.filter(
        item => JSON.stringify(item.params) !== JSON.stringify(params)
      );

      // Add new item and keep only the most recent searches
      const updatedHistory = [newItem, ...filteredHistory].slice(0, MAX_HISTORY_ITEMS);
      localStorage.setItem(SEARCH_HISTORY_KEY, JSON.stringify(updatedHistory));
    } catch (error) {
      console.error('Error saving search history:', error);
    }
  },

  clearSearchHistory(): void {
    try {
      localStorage.removeItem(SEARCH_HISTORY_KEY);
    } catch (error) {
      console.error('Error clearing search history:', error);
    }
  },

  // Location Autocomplete
  async getLocationSuggestions(query: string): Promise<string[]> {
    try {
      const response = await fetch(
        `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(query)}.json?access_token=${process.env.REACT_APP_MAPBOX_TOKEN}`
      );
      const data = await response.json();
      return data.features.map((feature: any) => feature.place_name);
    } catch (error) {
      console.error('Error fetching location suggestions:', error);
      return [];
    }
  },

  // Job Suggestions
  async getJobSuggestions(userId: string): Promise<JobSuggestion[]> {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/jobs/suggestions/${userId}`);
      return await response.json();
    } catch (error) {
      console.error('Error fetching job suggestions:', error);
      return [];
    }
  },

  // Advanced Filters
  getAdvancedFilters() {
    return {
      skills: [
        'JavaScript',
        'Python',
        'Java',
        'React',
        'Node.js',
        'SQL',
        'AWS',
        'Docker',
        'Kubernetes',
        'Machine Learning'
      ],
      industries: [
        'Technology',
        'Healthcare',
        'Finance',
        'Education',
        'Manufacturing',
        'Retail',
        'Real Estate',
        'Transportation',
        'Energy',
        'Agriculture'
      ],
      benefits: [
        'Health Insurance',
        'Dental Insurance',
        'Vision Insurance',
        '401(k)',
        'Paid Time Off',
        'Remote Work',
        'Flexible Hours',
        'Professional Development',
        'Stock Options',
        'Gym Membership'
      ],
      workEnvironments: [
        'Office',
        'Remote',
        'Hybrid',
        'On-site',
        'Travel Required',
        'Work from Home',
        'Flexible Location'
      ]
    };
  }
};

export default searchService; 