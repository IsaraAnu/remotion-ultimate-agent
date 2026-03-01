import { Composition } from 'remotion';
import { MyVideo } from './MyVideo';
export const RemotionRoot: React.FC = () => {
  return (<><Composition id="MyVideo" component={MyVideo} durationInFrames={1200} fps={60} width={1920} height={1080} /></>);
};