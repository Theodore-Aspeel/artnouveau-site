import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, useCurrentFrame} from 'remotion';
import master from '../assets/maison_coilliot_master_clean_candidate_v2.png';

const READ_END_FRAME = 18;
const MOVE_END_FRAME = 132;
const FINAL_SCALE = 1.35;
const FINAL_TRANSLATE_Y_PX = -128;

const cameraProgress = (frame: number): number =>
  interpolate(frame, [READ_END_FRAME, MOVE_END_FRAME], [0, 1], {
    easing: Easing.inOut(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

export const MaisonCoilliotStandardSpike: React.FC = () => {
  const frame = useCurrentFrame();
  const progress = cameraProgress(frame);
  const scale = interpolate(progress, [0, 1], [1, FINAL_SCALE]);
  const translateY = interpolate(progress, [0, 1], [0, FINAL_TRANSLATE_Y_PX]);

  return (
    <AbsoluteFill style={{backgroundColor: '#f4ead3', overflow: 'hidden'}}>
      <Img
        src={master}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: `translate3d(0, ${translateY}px, 0) scale(${scale})`,
          transformOrigin: '50% 50%',
        }}
      />
    </AbsoluteFill>
  );
};
