import React, { Component } from 'react'
// import Popup from './Popup/Popup'
// import ReactTooltip from 'react-tooltip'

class Highlight extends Component {
    constructor(props) {
        super(props)

        this.state = {
            content: '',
            links: [],
            showTooltip: false
        }
    }

    componentDidMount() {
        const { content, links } = this.props.mark.toJSON().data.keyword

        this.setState({
            content: content,
            links: links
        })
    }

    onMouseEnter = (e) => {
        e.preventDefault()

        this.setState({ showTooltip: true })
    }

    onMouseLeave = (e) => {
        e.preventDefault()

        this.setState({ showTooltip: false })
    }

    onClick = (e) => {
        e.preventDefault()

        this.props.setResults(this.state.links)
    }
 
    render() {
        const { children, attributes, color } = this.props

        const style = {
            'backgroundColor': color,
            'color': 'black',
            'padding': '.3em',
            'cursor': 'pointer'
        }

        // return <span onMouseEnter={this.onHover} style={style} {...{ attributes }}>{children}</span>

        // console.log(this.showTooltip)
        // if( this.state.showTooltip ) {
        //     console.log('displaying tooltip')
        //     return (
        //         <div>
        //             <Popup />
        //             {/* <ReactTooltip id='sadFace' type='warning' effect='solid'>
        //             <span>Show sad face</span>
        //         </ReactTooltip> */}

        //             <span onMouseEnter={this.onMouseEnter} onMouseLeave={this.onMouseLeave} style={style} {...{ attributes }}>{children}</span>
        //         </div>
        //     )
        // } else {
        //     return <span onMouseEnter={this.onMouseEnter} onMouseLeave={this.onMouseLeave} style={style} {...{ attributes }}>{children}</span>
        // }

        return (
            <span onClick={this.onClick} onMouseEnter={this.onMouseEnter} onMouseLeave={this.onMouseLeave} style={style} {...{ attributes }}>{children}</span>
        )

        // return (
        //     <Popup trigger={<button> Trigger</button>} position="top center">
        //         <div>Popup content here !!</div>
        //     </Popup>
        // )
    }
}

export default Highlight