import LinearProgress from '@mui/material/LinearProgress';
import './linearProgress.css'


export default function LinearIndeterminate(props) {
  return (
    <div className='progress'>
        {props.animate? <LinearProgress color="success"/>
        : <LinearProgress color="success" sx={{ "& .MuiLinearProgress-bar": {transition: "none", animation: 'none'}}}/>}
    </div>
  );
}
