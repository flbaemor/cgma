const { LL1Parser } = require('../../cgmaparsery');
const { cfg, predict_sets } = require('../../cfg');
const { run: lexerRun } = require('../../cgmalexer');

module.exports = async (req, res) => {
    const { source_code } = req.body;

    // Run Lexer
    const [tokens, errors] = lexerRun('<stdin>', source_code);

    // If lexer found errors, return them immediately
    if (errors.length > 0) {
        return res.status(200).json({ success: false, errors: errors.map(error => error.as_string()) });
    }

    // Run Parser
    const parser = new LL1Parser(cfg, predict_sets);
    const [success, parse_errors] = parser.parse(tokens);

    // Return parsing errors if any
    if (!success) {
        return res.status(200).json({ success: false, errors: parse_errors });
    }

    res.status(200).json({ success: true, errors: [] });
};