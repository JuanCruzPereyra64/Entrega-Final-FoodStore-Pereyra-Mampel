import { motion } from 'framer-motion'

interface CardProps {
  children: React.ReactNode
  className?: string
  noPadding?: boolean
  onClick?: () => void
}

export function Card({ children, className = '', noPadding = false, onClick }: CardProps) {
  return (
    <motion.div
      whileHover={onClick ? { y: -4, scale: 1.01 } : undefined}
      onClick={onClick}
      className={`premium-card ${noPadding ? '' : 'p-6'} ${onClick ? 'cursor-pointer' : ''} ${className}`}
    >
      {children}
    </motion.div>
  )
}

export function CardHeader({ title, subtitle, action }: { title: string; subtitle?: string; action?: React.ReactNode }) {
  return (
    <div className="flex items-center justify-between mb-6">
      <div>
        <h3 className="text-lg font-display font-semibold text-slate-900 dark:text-white">{title}</h3>
        {subtitle && <p className="text-sm text-slate-500 dark:text-slate-400 mt-0.5">{subtitle}</p>}
      </div>
      {action && <div>{action}</div>}
    </div>
  )
}
