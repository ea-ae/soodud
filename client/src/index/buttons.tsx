import React from 'react';

const CloseButton = (props: {onClose: () => void}) => {
    return (
        <div className="z-10 relative h-0 w-0">
            <span className="material-icons material-icon top-0 left-0 m-1
                             text-left text-neutral-600 hover:text-black text-3xl leading-none"
                    onClick={props.onClose}>close</span>
        </div>
    );
}

export default CloseButton;
