import React, { Component } from 'react'

class Highlight extends Component {
    constructor(props) {
        super(props)

        this.state = {
            content: '',
            links: []
        }
    }

    componentDidMount() {
        const { content, links } = this.props.mark.toJSON().data.keyword

        this.setState({
            content: content,
            links: links
        })
    }

    onHover = (e) => {
        e.preventDefault()

        console.log('highlight hover...', e.target.textContent)
    }
 
    render() {
        const { children, attributes, color } = this.props

        const style = {
            'backgroundColor': color,
            'color': 'black'
        }

        return <span onMouseEnter={this.onHover} style={style} {...{ attributes }}>{children}</span>
    }
}

export default Highlight