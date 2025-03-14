import React, { useState, useRef, useEffect } from 'react';
import { X, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

interface AutocompleteTagsProps {
  value: string[];
  onChange: (values: string[]) => void;
  suggestions?: { id: number; name: string; category?: string | null }[];
  placeholder?: string;
  className?: string;
  isLoading?: boolean;
  maxLength?: number;
  label?: string;
}

export function AutocompleteTags({
  value,
  onChange,
  suggestions = [],
  placeholder,
  className,
  isLoading = false,
  maxLength = 50,
  label,
}: AutocompleteTagsProps) {
  const [inputValue, setInputValue] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [filteredSuggestions, setFilteredSuggestions] = useState(suggestions);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const filtered = suggestions.filter(
      (suggestion) =>
        suggestion.name.toLowerCase().includes(inputValue.toLowerCase()) &&
        !value.includes(suggestion.name)
    );
    setFilteredSuggestions(filtered);
  }, [inputValue, suggestions, value]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        containerRef.current &&
        !containerRef.current.contains(event.target as Node)
      ) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      addTag(inputValue);
    } else if (e.key === 'Backspace' && !inputValue && value.length > 0) {
      onChange(value.slice(0, -1));
    }
  };

  const validateTag = (tag: string) => {
    return tag.length <= maxLength && /^[a-zA-Z0-9\s\-+#.]+$/.test(tag);
  };

  const addTag = (tag: string) => {
    const trimmedTag = tag.trim();
    if (
      trimmedTag &&
      !value.includes(trimmedTag) &&
      validateTag(trimmedTag)
    ) {
      onChange([...value, trimmedTag]);
      setInputValue('');
      setShowSuggestions(false);
    }
  };

  const removeTag = (tagToRemove: string) => {
    onChange(value.filter((tag) => tag !== tagToRemove));
  };

  return (
    <div ref={containerRef} className="relative">
      <div
        className={cn(
          'flex flex-wrap gap-2 p-2 border rounded-md bg-white min-h-[42px]',
          isLoading && 'opacity-70',
          className
        )}
      >
        {value.map((tag) => (
          <span
            key={tag}
            className="flex items-center gap-1 px-2 py-1 text-sm bg-blue-100 text-blue-800 rounded-md"
          >
            {tag}
            <button
              type="button"
              onClick={() => removeTag(tag)}
              className="text-blue-600 hover:text-blue-800"
              disabled={isLoading}
            >
              <X className="h-3 w-3" />
            </button>
          </span>
        ))}
        <div className="flex-1 relative">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => {
              setInputValue(e.target.value);
              setShowSuggestions(true);
            }}
            onKeyDown={handleKeyDown}
            onFocus={() => setShowSuggestions(true)}
            placeholder={value.length === 0 ? placeholder : ''}
            className="outline-none bg-transparent min-w-[120px] w-full"
            disabled={isLoading}
          />
          {isLoading && (
            <div className="absolute right-2 top-1/2 transform -translate-y-1/2">
              <Loader2 className="h-4 w-4 animate-spin text-gray-400" />
            </div>
          )}
        </div>
      </div>

      {showSuggestions && filteredSuggestions.length > 0 && (
        <div className="absolute z-50 w-full mt-1 bg-white border rounded-md shadow-lg max-h-[200px] overflow-y-auto">
          {filteredSuggestions.map((suggestion) => (
            <button
              key={suggestion.id}
              type="button"
              onClick={() => {
                addTag(suggestion.name);
              }}
              className="flex items-center gap-2 px-3 py-2 text-sm w-full text-left hover:bg-gray-100 focus:bg-gray-100 focus:outline-none"
            >
              <span>{suggestion.name}</span>
              {suggestion.category && (
                <span className="text-xs text-gray-500">
                  ({suggestion.category})
                </span>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
} 