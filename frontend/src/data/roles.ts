export interface RoleLevel { key: string; label: string; title: string }
export interface RoleGroup { id: string; label: string; blurb: string; levels: RoleLevel[] }

/**
 * Every `key` here must exist as a scorecard in the backend
 * (app/scorecard/scorecard.yaml or role_families.yaml). tests/unit/test_roles_sync.py
 * keeps the two in sync.
 */
export const ROLE_GROUPS: RoleGroup[] = [
  {
    id: 'dev', label: 'Developer', blurb: 'Software engineering',
    levels: [
      { key: 'trainee_dev', label: 'Trainee', title: 'Trainee Developer' },
      { key: 'junior_dev', label: 'Junior', title: 'Junior Developer' },
      { key: 'mid_dev', label: 'Mid', title: 'Developer' },
      { key: 'senior_dev', label: 'Senior', title: 'Senior Developer' },
      { key: 'staff_dev', label: 'Staff', title: 'Staff Developer' },
      { key: 'principal_dev', label: 'Principal', title: 'Principal Developer' },
    ],
  },
  {
    id: 'qa', label: 'QA Engineer', blurb: 'Quality & test automation',
    levels: [
      { key: 'trainee_qa', label: 'Trainee', title: 'Trainee QA Engineer' },
      { key: 'junior_qa', label: 'Junior', title: 'Junior QA Engineer' },
      { key: 'mid_qa', label: 'Mid', title: 'QA Engineer' },
      { key: 'senior_qa', label: 'Senior', title: 'Senior QA Engineer' },
      { key: 'staff_qa', label: 'Staff', title: 'Staff QA Engineer' },
      { key: 'principal_qa', label: 'Principal', title: 'Principal QA Engineer' },
    ],
  },
  {
    id: 'devops', label: 'DevOps Engineer', blurb: 'CI/CD, cloud & reliability',
    levels: [
      { key: 'junior_devops', label: 'Junior', title: 'Junior DevOps Engineer' },
      { key: 'mid_devops', label: 'Mid', title: 'DevOps Engineer' },
      { key: 'senior_devops', label: 'Senior', title: 'Senior DevOps Engineer' },
      { key: 'staff_devops', label: 'Staff', title: 'Staff DevOps / Platform Engineer' },
    ],
  },
  {
    id: 'security', label: 'Security Specialist', blurb: 'Application & infrastructure security',
    levels: [
      { key: 'junior_security', label: 'Junior', title: 'Junior Security Engineer' },
      { key: 'mid_security', label: 'Mid', title: 'Security Engineer' },
      { key: 'senior_security', label: 'Senior', title: 'Senior Security Engineer' },
      { key: 'staff_security', label: 'Staff', title: 'Staff Security Engineer' },
    ],
  },
  {
    id: 'po', label: 'Product Owner', blurb: 'Backlog & delivery with the team',
    levels: [
      { key: 'associate_po', label: 'Associate', title: 'Associate Product Owner' },
      { key: 'po', label: 'PO', title: 'Product Owner' },
      { key: 'senior_po', label: 'Senior', title: 'Senior Product Owner' },
      { key: 'lead_po', label: 'Lead', title: 'Lead Product Owner' },
      { key: 'principal_po', label: 'Principal', title: 'Principal Product Owner' },
    ],
  },
  {
    id: 'prodm', label: 'Product Manager', blurb: 'Strategy, discovery & outcomes',
    levels: [
      { key: 'associate_prodm', label: 'Associate', title: 'Associate Product Manager' },
      { key: 'mid_prodm', label: 'Mid', title: 'Product Manager' },
      { key: 'senior_prodm', label: 'Senior', title: 'Senior Product Manager' },
      { key: 'principal_prodm', label: 'Principal', title: 'Principal Product Manager' },
    ],
  },
  {
    id: 'pm', label: 'Project Manager', blurb: 'Planning, risk & delivery',
    levels: [
      { key: 'junior_pm', label: 'Junior', title: 'Junior Project Manager' },
      { key: 'mid_pm', label: 'Mid', title: 'Project Manager' },
      { key: 'senior_pm', label: 'Senior', title: 'Senior Project Manager' },
      { key: 'lead_pm', label: 'Lead', title: 'Program Manager' },
    ],
  },
  {
    id: 'hr', label: 'HR / People', blurb: 'People operations & business partnering',
    levels: [
      { key: 'associate_hr', label: 'Associate', title: 'HR Associate / Coordinator' },
      { key: 'generalist_hr', label: 'Generalist', title: 'HR Generalist / Business Partner' },
      { key: 'senior_hr', label: 'Senior', title: 'Senior HR Business Partner' },
      { key: 'lead_hr', label: 'Lead', title: 'HR Lead / Head of People' },
    ],
  },
]

export function findRole(key: string): { group: RoleGroup; level: RoleLevel } | null {
  for (const group of ROLE_GROUPS) {
    const level = group.levels.find(l => l.key === key)
    if (level) return { group, level }
  }
  return null
}
