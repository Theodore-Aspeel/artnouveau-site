import React from 'react';
import {Composition} from 'remotion';
import {MaisonCoilliotStandardSpike} from './MaisonCoilliotStandardSpike';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="MaisonCoilliotStandardSpike"
      component={MaisonCoilliotStandardSpike}
      durationInFrames={150}
      fps={30}
      width={720}
      height={1280}
    />
  );
};
