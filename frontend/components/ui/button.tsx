import * as React from "react"
import { cn } from "@/utils/cn"

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost' | 'destructive'
  size?: 'default' | 'sm' | 'lg' | 'icon'
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', size = 'default', ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50 active:scale-95 duration-100",
          variant === 'default' && "bg-blue-600 text-white hover:bg-blue-700",
          variant === 'outline' && "border border-zinc-700 hover:bg-zinc-800 text-zinc-200",
          variant === 'ghost' && "hover:bg-zinc-850 text-zinc-300",
          variant === 'destructive' && "bg-red-600 text-white hover:bg-red-700",
          size === 'default' && "h-10 px-4 py-2",
          size === 'sm' && "h-8 px-3 text-xs",
          size === 'lg' && "h-12 px-8",
          size === 'icon' && "h-10 w-10",
          className
        )}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button }
