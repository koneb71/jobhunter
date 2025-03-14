"use client"

import * as React from "react"
import { Circle } from "lucide-react"
import { cn } from "@/lib/utils"

interface RadioGroupProps extends React.HTMLAttributes<HTMLDivElement> {
  value?: string
  onValueChange?: (value: string) => void
}

const RadioGroup = React.forwardRef<HTMLDivElement, RadioGroupProps>(
  ({ className, value, onValueChange, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn("grid gap-2", className)}
        role="radiogroup"
        {...props}
      />
    )
  }
)
RadioGroup.displayName = "RadioGroup"

interface RadioGroupItemProps extends React.InputHTMLAttributes<HTMLInputElement> {
  value: string
}

const RadioGroupItem = React.forwardRef<HTMLInputElement, RadioGroupItemProps>(
  ({ className, value, ...props }, ref) => {
    const radioGroup = React.useContext(RadioGroupContext)
    const checked = radioGroup?.value === value

    return (
      <div className="relative inline-flex items-center">
        <input
          type="radio"
          ref={ref}
          value={value}
          checked={checked}
          onChange={(e) => radioGroup?.onValueChange?.(e.target.value)}
          className="peer sr-only"
          {...props}
        />
        <div
          className={cn(
            "aspect-square h-4 w-4 rounded-full border border-primary text-primary shadow focus:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50",
            checked && "bg-primary text-primary-foreground",
            className
          )}
        >
          {checked && (
            <Circle className="h-2.5 w-2.5 fill-current text-current" />
          )}
        </div>
      </div>
    )
  }
)
RadioGroupItem.displayName = "RadioGroupItem"

const RadioGroupContext = React.createContext<RadioGroupProps | null>(null)

export { RadioGroup, RadioGroupItem }
