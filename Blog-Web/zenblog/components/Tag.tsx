import React from 'react';

interface TagProps {
  label: string;
  onClick?: () => void;
  isActive?: boolean;
}

export const Tag: React.FC<TagProps> = ({ label, onClick, isActive }) => {
  return (
    <span 
      onClick={onClick}
      className={`
        inline-block px-3 py-1 text-xs font-medium rounded-full cursor-pointer transition-colors duration-200 border
        ${isActive 
          ? 'bg-stone-800 text-white border-stone-800' 
          : 'bg-transparent text-stone-500 border-stone-300 hover:border-stone-500 hover:text-stone-700'}
      `}
    >
      #{label}
    </span>
  );
};