import {React} from 'react';
import {TailSpin} from 'react-loader-dom';
import './LoadingPage.css';

const LoadingPage = () => {
    return(
        <div className='loader-container'>
            <TailSpin 
                visible={True}
                height={100}
                width={100}
                color="#2D9596"
                ariaLabel="tail-spin-loading"
                radius={2}
            />
            <p className='loader-test'>문제 생성중</p>
        </div>
    );
};

export default LoadingPage