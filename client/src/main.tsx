import {render} from 'preact'
import Routing from "./utils/Router.tsx";
import './global.css';
import '@radix-ui/themes/styles.css';
import {Theme} from "@radix-ui/themes";

/**
 * Returns the pathname of the current Base URL
 * @return {string} The pathname
 */

render(<Theme
    appearance="dark"
    accentColor="violet"
    panelBackground="solid">
    <Routing/>
</Theme>, document.getElementById('app')!)
