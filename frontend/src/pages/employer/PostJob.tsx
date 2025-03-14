import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import { motion } from 'framer-motion';
import { Briefcase, MapPin, DollarSign, Building2, FileText } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { TagInput } from '@/components/ui/tag-input';
import { useJobs, CreateJobData } from '@/hooks/useJobs';
import { useSkills } from '@/hooks/useSkills';
import { useBenefits } from '@/hooks/useBenefits';
import { useAuthStore } from '@/stores/authStore';
import { AutocompleteTags } from '@/components/ui/autocomplete-tags';

const employmentTypes = [
  { value: 'full_time', label: 'Full Time' },
  { value: 'part_time', label: 'Part Time' },
  { value: 'contract', label: 'Contract' },
  { value: 'internship', label: 'Internship' },
  { value: 'temporary', label: 'Temporary' },
];

const experienceLevels = [
  { value: 'entry', label: 'Entry Level' },
  { value: 'mid', label: 'Mid Level' },
  { value: 'senior', label: 'Senior Level' },
  { value: 'lead', label: 'Lead' },
  { value: 'executive', label: 'Executive' },
];

const departments = [
  { value: 'engineering', label: 'Engineering' },
  { value: 'design', label: 'Design' },
  { value: 'product', label: 'Product' },
  { value: 'marketing', label: 'Marketing' },
  { value: 'sales', label: 'Sales' },
  { value: 'customer_support', label: 'Customer Support' },
  { value: 'hr', label: 'Human Resources' },
  { value: 'finance', label: 'Finance' },
  { value: 'operations', label: 'Operations' },
  { value: 'other', label: 'Other' },
];

export const PostJob: React.FC = () => {
  const navigate = useNavigate();
  const { createJob, isCreatingJob } = useJobs();
  const { skills, isLoading: isLoadingSkills, getOrCreateSkill } = useSkills();
  const { benefits, isLoading: isLoadingBenefits, getOrCreateBenefit } = useBenefits();
  const { user } = useAuthStore();

  const [formData, setFormData] = useState<CreateJobData>({
    title: '',
    description: '',
    company_id: user?.id || '',
    location: '',
    salary_range: '',
    employment_type: '',
    experience_level: '',
    skills_required: [],
    benefits: [],
    is_remote: false,
    is_featured: false,
    status: 'draft',
    department: '',
    remote_work: false,
    visa_sponsorship: false,
    relocation_assistance: false,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSelectChange = (name: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCheckboxChange = (name: string, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      [name]: checked
    }));
  };

  const handleSkillsChange = async (skillNames: string[]) => {
    try {
      const skillObjects = await Promise.all(
        skillNames.map(name => getOrCreateSkill(name))
      );
      
      setFormData(prev => ({
        ...prev,
        skills_required: skillObjects.map(skill => skill.id)
      }));
    } catch (error) {
      console.error('Error updating skills:', error);
      toast.error('Failed to update skills');
    }
  };

  const handleBenefitsChange = async (benefitNames: string[]) => {
    try {
      const benefitObjects = await Promise.all(
        benefitNames.map(name => getOrCreateBenefit(name))
      );
      
      setFormData(prev => ({
        ...prev,
        benefits: benefitObjects.map(benefit => benefit.id)
      }));
    } catch (error) {
      console.error('Error updating benefits:', error);
      toast.error('Failed to update benefits');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      if (!user?.id) {
        toast.error('Company ID is required');
        return;
      }

      await createJob(formData);
      toast.success('Job posted successfully!');
      navigate('/employer/dashboard');
    } catch (error) {
      console.error('Error posting job:', error);
      if (error instanceof Error) {
        toast.error(error.message);
      } else {
        toast.error('Failed to post job. Please try again.');
      }
    }
  };

  // Get the names of selected skills and benefits for display
  const selectedSkillNames = skills
    .filter(skill => formData.skills_required.includes(skill.id))
    .map(skill => skill.name);

  const selectedBenefitNames = benefits
    .filter(benefit => formData.benefits.includes(benefit.id))
    .map(benefit => benefit.name);

  return (
    <div className="container mx-auto px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-4xl mx-auto"
      >
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Post a New Job</h1>
          <Button
            variant="outline"
            onClick={() => navigate('/employer/dashboard')}
            className="flex items-center"
          >
            <Briefcase className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label htmlFor="title">Job Title</Label>
              <Input
                id="title"
                name="title"
                value={formData.title}
                onChange={handleChange}
                required
                placeholder="e.g., Senior Software Engineer"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="department">Department</Label>
              <Select
                value={formData.department}
                onValueChange={(value) => handleSelectChange('department', value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select department" />
                </SelectTrigger>
                <SelectContent>
                  {departments.map((dept) => (
                    <SelectItem key={dept.value} value={dept.value}>
                      {dept.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="location">Location</Label>
              <div className="relative">
                <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <Input
                  id="location"
                  name="location"
                  value={formData.location}
                  onChange={handleChange}
                  required
                  className="pl-10"
                  placeholder="e.g., New York, NY"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="employment_type">Employment Type</Label>
              <Select
                value={formData.employment_type}
                onValueChange={(value) => handleSelectChange('employment_type', value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select employment type" />
                </SelectTrigger>
                <SelectContent>
                  {employmentTypes.map((type) => (
                    <SelectItem key={type.value} value={type.value}>
                      {type.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="salary_range">Salary Range</Label>
              <div className="relative">
                <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <Input
                  id="salary_range"
                  name="salary_range"
                  value={formData.salary_range}
                  onChange={handleChange}
                  required
                  className="pl-10"
                  placeholder="e.g., $50,000 - $100,000"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="experience_level">Experience Level</Label>
              <Select
                value={formData.experience_level}
                onValueChange={(value) => handleSelectChange('experience_level', value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select experience level" />
                </SelectTrigger>
                <SelectContent>
                  {experienceLevels.map((level) => (
                    <SelectItem key={level.value} value={level.value}>
                      {level.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Job Description</Label>
            <Textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              className="min-h-[150px]"
              placeholder="Describe the role and its key responsibilities..."
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="skills_required">Required Skills</Label>
            <AutocompleteTags
              value={selectedSkillNames}
              onChange={handleSkillsChange}
              suggestions={skills.map(skill => ({
                id: skill.id,
                name: skill.name,
                category: skill.category
              }))}
              placeholder="Type a skill and press Enter..."
              className="min-h-[42px]"
              isLoading={isLoadingSkills}
              maxLength={100}
            />
            <p className="text-sm text-gray-500">
              {isLoadingSkills 
                ? 'Loading skills...' 
                : 'Type to search or add new skills. Press Enter to add.'}
            </p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="benefits">Benefits</Label>
            <AutocompleteTags
              value={selectedBenefitNames}
              onChange={handleBenefitsChange}
              suggestions={benefits.map(benefit => ({
                id: benefit.id,
                name: benefit.name,
                category: benefit.category
              }))}
              placeholder="Type a benefit and press Enter..."
              className="min-h-[42px]"
              isLoading={isLoadingBenefits}
              maxLength={100}
            />
            <p className="text-sm text-gray-500">
              {isLoadingBenefits 
                ? 'Loading benefits...' 
                : 'Type to search or add new benefits. Press Enter to add.'}
            </p>
          </div>

          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Checkbox
                id="is_remote"
                checked={formData.is_remote}
                onCheckedChange={(checked) => handleCheckboxChange('is_remote', checked as boolean)}
              />
              <Label htmlFor="is_remote">Remote Job</Label>
            </div>

            <div className="flex items-center space-x-2">
              <Checkbox
                id="remote_work"
                checked={formData.remote_work}
                onCheckedChange={(checked) => handleCheckboxChange('remote_work', checked as boolean)}
              />
              <Label htmlFor="remote_work">Remote Work Available</Label>
            </div>

            <div className="flex items-center space-x-2">
              <Checkbox
                id="visa_sponsorship"
                checked={formData.visa_sponsorship}
                onCheckedChange={(checked) => handleCheckboxChange('visa_sponsorship', checked as boolean)}
              />
              <Label htmlFor="visa_sponsorship">Visa Sponsorship Available</Label>
            </div>

            <div className="flex items-center space-x-2">
              <Checkbox
                id="relocation_assistance"
                checked={formData.relocation_assistance}
                onCheckedChange={(checked) => handleCheckboxChange('relocation_assistance', checked as boolean)}
              />
              <Label htmlFor="relocation_assistance">Relocation Assistance Available</Label>
            </div>

            <div className="flex items-center space-x-2">
              <Checkbox
                id="is_featured"
                checked={formData.is_featured}
                onCheckedChange={(checked) => handleCheckboxChange('is_featured', checked as boolean)}
              />
              <Label htmlFor="is_featured">Feature this Job Posting</Label>
            </div>
          </div>

          <div className="flex justify-end space-x-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate('/employer/dashboard')}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={isCreatingJob}
              className="bg-blue-600 hover:bg-blue-700"
            >
              {isCreatingJob ? 'Posting...' : 'Post Job'}
            </Button>
          </div>
        </form>
      </motion.div>
    </div>
  );
};