import { motion } from 'framer-motion'
import type { LucideIcon } from 'lucide-react'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'accent' | 'danger' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  icon?: LucideIcon
  isLoading?: boolean
}

export function Button({
  children,
  variant = 'primary',
  size = 'md',
  icon: Icon,
  isLoading,
  className = '',
  ...props
}: ButtonProps) {
  const baseStyles = 'inline-flex items-center justify-center font-medium transition-all duration-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed'
  
  const variants = {
    primary: 'bg-primary text-white hover:bg-primary-hover shadow-lg shadow-primary/20 focus:ring-primary',
    secondary: 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700 focus:ring-slate-400',
    accent: 'bg-accent text-white hover:bg-accent-hover shadow-lg shadow-accent/20 focus:ring-accent',
    danger: 'bg-red-500 text-white hover:bg-red-600 shadow-lg shadow-red-500/20 focus:ring-red-500',
    ghost: 'bg-transparent text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 focus:ring-slate-400'
  }
  
  const sizes = {
    sm: 'px-3 py-1.5 text-xs gap-1.5',
    md: 'px-4 py-2 text-sm gap-2',
    lg: 'px-6 py-3 text-base gap-2.5'
  }

  // To fix the TS error with motion.button and regular button props
  // we cast to any or define the specific subset of props that motion accepts.
  // For this simple case, casting the component or the props usually works best in a pinch.
  const MotionButton = motion.button as any;

  return (
    <MotionButton
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      disabled={isLoading || props.disabled}
      {...props}
    >
      {isLoading ? (
        <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
      ) : Icon ? (
        <Icon size={size === 'sm' ? 14 : size === 'md' ? 18 : 22} />
      ) : null}
      {children}
    </MotionButton>
  )
}
