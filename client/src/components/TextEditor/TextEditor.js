import React, { Component } from 'react';
import './TextEditor.css';
import { Editor } from 'slate-react';
import { Value, Data } from 'slate';
import Highlight from '../Highlight';
import { TXT } from './sample.js';

const initialValue = Value.fromJSON({
    document: {
        nodes: [
            {
                object: 'block',
                type: 'paragraph',
                nodes: [
                    {
                        object: 'text',
                        leaves: [
                            {
                                text: TXT
                            }
                        ]
                    }
                ]
            }
        ]
    }
})

// const initialResults = () => {
//     return (
//         <div className="c-inital">
//             <h4>Google</h4>
//             <ul>
//                 <li><a href="">link</a></li>
//                 <li><a href="">link</a></li>
//                 <li><a href="">link</a></li>
//             </ul>
//         </div>
//     )
// }

const Results = (props) => {
    const { links } = props

    if( links.length ) {
        return (
            <div className="c-item">
                <h4>Google</h4>
                <ul>
                    { links.map(link => {
                        return <li><a target="_" href={link}>click me</a></li>
                    }) }
                </ul>
            </div>
        )
    } else {
        return (
            <div className="c-inital">
                Select a Section and Press <em>Ctrl+H</em> to analysis
            </div>
        )
    }
    
}

// const initialResults = `
//     <div className="c-inital">
//         <h4>Google</h4>
//         <ul>
//             <li><a href="">link</a></li>
//             <li><a href="">link</a></li>
//             <li><a href="">link</a></li>
//         </ul>
//     </div>
// `

const results = {
    keywords: [
        {
            content: 'summer\'s lease hath',
            links: [
                'http://www.shakespeare-online.com/sonnets/18detail.html',
                'https://www.answers.com/Q/What_is_the_original_word_of_ow\'st',
                'https://www.sparknotes.com/nofear/shakespeare/sonnets/sonnet_18/'
            ]
        },
        {
            content: 'this gives life to thee.',
            links: [
                'https://www.shmoop.com/sonnet-18/section-2-lines-9-14-summary.html',
                'https://brainly.com/question/3697676'
            ]
        }
    ]
}

export default class TextEditor extends Component {

    schema = {
        marks: {
            highlight: {
                isAtomic: true,
            },
        },
    }

    decorations = []

    renderMark = (props, editor, next) => {
        const { children, mark, attributes } = props
        switch (mark.type) {
            case 'bold':
                return <strong {...{ attributes }}>{children}</strong>
            case 'italic':
                return <em {...{ attributes }}>{children}</em>
            case 'code':
                return <code {...{ attributes }}>{children}</code>
            case 'underline':
                return <u {...{ attributes }}>{children}</u>
            case 'strikethrough':
                return <strike {...{ attributes }}>{children}</strike>
            case 'highlight':
                return <Highlight {...props} color="yellow" setResults={this.setResults} />
            default:
                return next()
        }
    }

    markPlugin() {
        return {
            renderMark: this.renderMark
        }
    }

    plugins = [
        this.markPlugin()
    ]

    /**
     * Store a reference to the `editor`.
     *
     * @param {Editor} editor
     */

    ref = editor => {
        this.editor = editor
    }
    
    constructor(props) {
        super(props)

        this.state = {
            value: initialValue,
            links: []
        }
    }

    componentDidMount() {
        this.mapKeywords(results.keywords)
    }

    mapKeywords = (keywords) => {
        keywords.map(keyword => {
            this.highlight(keyword)
        })
    }

    highlight(keyword, color = 'yellow') {
        const { editor } = this
        const { content } = keyword
        const { value } = editor
        const texts = value.document.getTexts()
        // const decorations = []

        texts.forEach(node => {
            const { key, text } = node
            const parts = text.split(content)
            let offset = 0

            parts.forEach((part, i) => {
                if (i !== 0) {
                    this.decorations.push({
                        anchor: { key, offset: offset - content.length },
                        focus: { key, offset },
                        mark: { type: 'highlight', data: Data.fromJSON({ keyword }) },
                    })
                }

                offset = offset + part.length + content.length
            })
        })

        // console.log(decorations, str)

        editor.withoutSaving(() => {
            editor.setDecorations(this.decorations)
        })
    }

    setResults = (links) => {
        this.setState({links})
    }

    onChange = ({ value }) => {
        this.setState({ value })
    }

    onKeyDown = (e, editor, next) => {
        // cancel actions not starting with Ctrl key press
        if(! e.ctrlKey )    return next()
        e.preventDefault()

        switch (e.key) {
            case 'b': {
                editor.toggleMark('bold')
                return true
            }
            case 'h': {
                editor.toggleMark('highlight')
                return true
            }
            default:
                return next()
        }
    }

    render() {
        // let RESULTS
        // if( this.state.results !== '' ) {
        //     RESULTS = <initialResults />
        // } else {
        //     RESULTS = 'dd'
        // }

        return(
            <div className="c-main">
                <div className="c-text">
                    <Editor
                        plugins={this.plugins}
                        ref={this.ref}
                        defaultValue={this.state.value}
                        schema={this.schema}
                        onChange={this.onChange}
                        onKeyDown={this.onKeyDown}
                    />
                </div>
                <div className="c-results">
                    {/* <i class="fas fa-igloo"></i> */}
                    <Results links={this.state.links} />
                </div>
            </div>
        )
    }
} 