import React from 'react';
import { DerivationsBrowser } from '@/components/Derivations/DerivationsBrowser';
import './Derivations.scss';

const Derivations: React.FC = () => {
  return (
    <div className="derivations-page">
      <DerivationsBrowser />
    </div>
  );
};

export default Derivations;
