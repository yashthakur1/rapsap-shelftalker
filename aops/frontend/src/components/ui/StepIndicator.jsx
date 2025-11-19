import React from 'react';
import { Check } from 'lucide-react';
import { cn } from '../../lib/utils';

const steps = [
  { number: 1, label: 'Upload CSV' },
  { number: 2, label: 'Select Template' },
  { number: 3, label: 'Preview' },
  { number: 4, label: 'Download' },
];

export default function StepIndicator({ currentStep }) {
  return (
    <div className="w-full max-w-4xl mx-auto py-8">
      <div className="flex items-center justify-between">
        {steps.map((step, index) => (
          <React.Fragment key={step.number}>
            {/* Step Circle */}
            <div className="flex flex-col items-center">
              <div
                className={cn(
                  'w-12 h-12 rounded-full flex items-center justify-center font-semibold transition-all',
                  currentStep > step.number
                    ? 'bg-green-500 text-white'
                    : currentStep === step.number
                    ? 'bg-primary text-white ring-4 ring-primary/20'
                    : 'bg-gray-200 text-gray-500'
                )}
              >
                {currentStep > step.number ? (
                  <Check className="w-6 h-6" />
                ) : (
                  step.number
                )}
              </div>
              <span
                className={cn(
                  'mt-2 text-sm font-medium',
                  currentStep >= step.number ? 'text-foreground' : 'text-muted-foreground'
                )}
              >
                {step.label}
              </span>
            </div>

            {/* Connector Line */}
            {index < steps.length - 1 && (
              <div
                className={cn(
                  'flex-1 h-1 mx-4 rounded transition-all',
                  currentStep > step.number ? 'bg-green-500' : 'bg-gray-200'
                )}
              />
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}
