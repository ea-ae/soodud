import React from 'react';


const ProductHeader = (props: {stores: string[], item_layout: string}) => {
    return ( // removed: px-1.5 sm:px-3
        <>
        <MenuButton />
        <div className="group flex justify-center md:justify-end items-center justify-items-center
                        sticky top-0 flex-wrap md:flex-nowrap mx-1.5 sm:mx-3 lg:mx-5 py-2 bg-stone-50 text-stone-600">
            <div className="flex justify-center md:justify-end flex-grow min-w-[5em] mt-1 md:mt-0 ml-1">
                <span className="mr-3 text-stone-900 text-xs">Tavahind</span>
                <span className="mr-3 text-yellow-400 text-xs">Soodustus</span>
                <span className="md:mr-6 text-amber-500 text-xs">Kliendikaardiga</span>
            </div>
            <div className="basis-full md:basis-0 md:hidden"></div>
            {props.stores.sort().map(
                store => <ProductHeaderColumn key={store} storeName={store} item_layout={props.item_layout} />)}
        </div>
        </>
    );
}

const MenuButton = () => { // basis-full
    return (
        <div className="z-10 relative h-0 w-0">
             <span className="material-icons material-icon absolute top-0 left-0 m-1.5 sm:m-3
                              text-left text-neutral-900 text-2xl leading-none"
                   onClick={e => console.log('menu')}>menu</span>
        </div>
    );
}

const ProductHeaderColumn = (props: {storeName: string, item_layout: string}) => {
    return (
        <div className={props.item_layout}>
            <span className="text-xs lg:text-sm">{props.storeName}</span>
        </div>
    );
}

export default ProductHeader;
