import React from 'react';
import Popup from 'reactjs-popup';

import CloseButton from './buttons';


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
    const menuButton = <span className="material-icons material-icon absolute top-0 left-0 m-1.5 sm:m-3
                                        text-left text-neutral-600 hover:text-black text-2xl leading-none">menu</span>

    return (
        <div className="z-10 relative h-0 w-0">
             <Popup trigger={menuButton} modal>
                {(onClose: () => void) => (
                    <div className="shadow-xl border w-[90vw] md:w-[80vw] xl:w-[60vw] bg-stone-50 font-main text-neutral-800">
                        <CloseButton onClose={onClose} />
                        <div className="flex flex-col justify-center items-center">
                            <p className="px-12 pt-16 align-middle">
                                Tootehinnad on uuendatud korra päevas ja kehtivad ainult e-poodidele.
                                E-poodides leiduvad hinnad ja kampaaniad ei kajasta alati kohalolevaid pakkumisi.
                                Tooteanalüüsija ei ole alati võimeline ideaalselt ühendama poodide vahelisi tooteid,
                                mistõttu on alati kasulik kontrollida võrreldavaid tooted üle enne ostu. Ainult
                                Prisma ja Selveri e-poed avalikustavad oma toodete triipkoode, tänu millele on
                                võimalik nende kahe poe tooteid kokku sobitada 100% täpsusega.
                            </p>
                            <p className="px-12 py-8 align-middle">Kontakt: soodudee, gmail.</p>
                        </div>
                    </div>
                )}
             </Popup>
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
