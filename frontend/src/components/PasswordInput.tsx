import { useState } from 'react'

interface Props {
  name?: string
  placeholder?: string
  autoComplete?: string
  minLength?: number
  required?: boolean
}

/** Password field with an eye button that toggles between hidden and visible text. */
export default function PasswordInput({
  name = 'password',
  placeholder = 'Password',
  autoComplete,
  minLength,
  required = true,
}: Props) {
  const [visible, setVisible] = useState(false)

  return (
    <div className="relative">
      <input
        name={name}
        type={visible ? 'text' : 'password'}
        placeholder={placeholder}
        autoComplete={autoComplete}
        minLength={minLength}
        required={required}
        className="w-full border border-slate-300 rounded-lg pl-3 pr-12 py-3 text-base bg-white"
      />
      <button
        type="button"
        onClick={() => setVisible((v) => !v)}
        aria-label={visible ? 'Hide password' : 'Show password'}
        aria-pressed={visible}
        className="absolute inset-y-0 right-0 flex items-center px-3 text-slate-500 hover:text-slate-900"
      >
        {visible ? (
          // eye-off
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor"
            strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M17.94 17.94A10.94 10.94 0 0 1 12 20C5 20 1 12 1 12a18.5 18.5 0 0 1 5.06-5.94" />
            <path d="M9.9 4.24A10.94 10.94 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19" />
            <path d="M14.12 14.12a3 3 0 1 1-4.24-4.24" />
            <line x1="1" y1="1" x2="23" y2="23" />
          </svg>
        ) : (
          // eye
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor"
            strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
            <circle cx="12" cy="12" r="3" />
          </svg>
        )}
      </button>
    </div>
  )
}
