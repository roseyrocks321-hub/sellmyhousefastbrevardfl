<?php
/**
 * Plugin Name: GTR Free Performance Boost
 * Description: Auto-loaded performance optimizations. No config needed.
 * Version: 1.0
 * Author: Hermes Auto
 */

if (!defined('ABSPATH')) exit;

// 1. DEFER non-critical JS
add_filter('script_loader_tag', function($tag, $handle) {
    $defer_handles = ['jquery-core', 'jquery-migrate', 'wp-embed', 'wpemoji'];
    $async_handles = [];
    
    foreach ($defer_handles as $h) {
        if (strpos($handle, $h) !== false && strpos($tag, 'defer') === false) {
            return str_replace(' src=', ' defer src=', $tag);
        }
    }
    return $tag;
}, 10, 2);

// 2. NATIVE LAZY LOAD for all images
add_filter('wp_img_tag_add_loading_attr', function($value) {
    return 'lazy';
}, 10);

add_filter('the_content', function($content) {
    if (is_admin()) return $content;
    return preg_replace('/<img([^>]+)>/i', '<img$1 loading="lazy">', $content);
});

// 3. REMOVE WP BLOAT
remove_action('wp_head', 'wp_generator');
remove_action('wp_head', 'rsd_link');
remove_action('wp_head', 'wlwmanifest_link');
remove_action('wp_head', 'wp_shortlink_wp_head');
remove_action('wp_head', 'rest_output_link_wp_head');
remove_action('wp_head', 'wp_oembed_add_discovery_links');
remove_action('template_redirect', 'rest_output_link_header', 11);
remove_action('wp_head', 'print_emoji_detection_script', 7);
remove_action('admin_print_scripts', 'print_emoji_detection_script');
remove_action('wp_print_styles', 'print_emoji_styles');
remove_action('admin_print_styles', 'print_emoji_styles');
remove_filter('the_content_feed', 'wp_staticize_emoji');
remove_filter('comment_text_rss', 'wp_staticize_emoji');
remove_filter('wp_mail', 'wp_staticize_emoji_for_email');
add_filter('emoji_svg_url', '__return_false');
add_filter('tiny_mce_plugins', function($plugins) {
    return is_array($plugins) ? array_diff($plugins, ['wpemoji']) : [];
});

// Disable embeds
function gtr_disable_embeds() {
    wp_deregister_script('wp-embed');
}
add_action('wp_footer', 'gtr_disable_embeds');

// 4. DNS PRECONECT + PRECONNECT
add_action('wp_head', function() {
    echo "<link rel='dns-prefetch' href='//fonts.googleapis.com' />\n";
    echo "<link rel='preconnect' href='https://fonts.gstatic.com' crossorigin />\n";
    echo "<link rel='preconnect' href='https://www.googletagmanager.com' crossorigin />\n";
    echo "<link rel='preconnect' href='https://www.google-analytics.com' crossorigin />\n";
}, 1);

// 5. DISABLE HEARTBEAT API (reduces admin-ajax calls)
add_action('init', function() {
    wp_deregister_script('heartbeat');
}, 1);

// 6. DISABLE XML-RPC
add_filter('xmlrpc_enabled', '__return_false');
add_filter('wp_headers', function($headers) {
    unset($headers['X-Pingback']);
    return $headers;
});

// 7. REMOVE QUERY STRINGS from static resources
add_filter('script_loader_src', 'gtr_remove_query_strings', 15);
add_filter('style_loader_src', 'gtr_remove_query_strings', 15);
function gtr_remove_query_strings($src) {
    if (strpos($src, '?ver=')) $src = remove_query_arg('ver', $src);
    if (strpos($src, '?v=')) $src = remove_query_arg('v', $src);
    return $src;
}

// 8. LIMIT POST REVISIONS (keeps DB lean)
if (!defined('WP_POST_REVISIONS')) define('WP_POST_REVISIONS', 3);

// 9. DISABLE SELF-PINGBACKS
add_action('pre_ping', function(&$links) {
    $home = get_option('home');
    foreach ($links as $l => $link) {
        if (strpos($link, $home) === 0) unset($links[$l]);
    }
});

// 10. ADD FETCHPRIORITY to hero/LCP image (auto-detect first image)
add_filter('wp_get_attachment_image_attributes', function($attr) {
    static $first = true;
    if ($first && isset($attr['class']) && strpos($attr['class'], 'attachment-large') !== false) {
        $attr['fetchpriority'] = 'high';
        $first = false;
    }
    return $attr;
});

// 11. JSON-LD SCHEMA: LocalBusiness + FAQPage + Organization
add_action('wp_head', function() {
    $site_url = 'https://goldenticketrealty.com';
    $local_business = [
        '@context' => 'https://schema.org',
        '@type' => 'LocalBusiness',
        '@id' => $site_url . '/#localbusiness',
        'name' => 'Golden Ticket Realty',
        'url' => $site_url,
        'telephone' => '+1-321-294-2081',
        'address' => [
            '@type' => 'PostalAddress',
            'addressLocality' => 'Melbourne',
            'addressRegion' => 'FL',
            'addressCountry' => 'US'
        ],
        'areaServed' => [
            '@type' => 'City',
            'name' => 'Melbourne, FL'
        ]
    ];

    $faq_page = [
        '@context' => 'https://schema.org',
        '@type' => 'FAQPage',
        'mainEntity' => [
            [
                '@type' => 'Question',
                'name' => 'How can I sell my house fast in Melbourne, FL?',
                'acceptedAnswer' => [
                    '@type' => 'Answer',
                    'text' => 'To sell your house fast in Melbourne, FL, consider working with a local cash home buyer like Golden Ticket Realty. We buy houses as-is, eliminating the need for repairs, showings, or waiting for buyer financing. Contact us at 321-294-2081 for a fair cash offer within 24 hours.'
                ]
            ],
            [
                '@type' => 'Question',
                'name' => 'Do I need to make repairs before selling my house in Melbourne?',
                'acceptedAnswer' => [
                    '@type' => 'Answer',
                    'text' => 'No, you do not need to make any repairs. Golden Ticket Realty purchases homes in any condition throughout Melbourne and the surrounding Brevard County area. We handle all repairs and cleanup after closing, saving you time and money.'
                ]
            ],
            [
                '@type' => 'Question',
                'name' => 'How quickly can I close when selling my house for cash in Melbourne?',
                'acceptedAnswer' => [
                    '@type' => 'Answer',
                    'text' => 'Golden Ticket Realty can close in as little as 7 to 14 days, depending on your timeline. Because we pay cash, there is no waiting for bank approvals or mortgage underwriting. You choose the closing date that works best for you.'
                ]
            ],
            [
                '@type' => 'Question',
                'name' => 'Will I pay any fees or commissions selling to Golden Ticket Realty?',
                'acceptedAnswer' => [
                    '@type' => 'Answer',
                    'text' => 'There are no realtor commissions, closing costs, or hidden fees when you sell directly to Golden Ticket Realty. The cash offer we present is the amount you receive at closing, making it one of the most transparent ways to sell your home in Melbourne, FL.'
                ]
            ],
            [
                '@type' => 'Question',
                'name' => 'What types of properties does Golden Ticket Realty buy in Melbourne?',
                'acceptedAnswer' => [
                    '@type' => 'Answer',
                    'text' => 'We buy single-family homes, condos, townhouses, multi-family properties, and vacant land across Melbourne, Palm Bay, Cocoa Beach, and all of Brevard County. Whether your property is move-in ready or needs major repairs, we are interested in making a cash offer.'
                ]
            ]
        ]
    ];

    $organization = [
        '@context' => 'https://schema.org',
        '@type' => 'Organization',
        '@id' => $site_url . '/#organization',
        'name' => 'Golden Ticket Realty',
        'url' => $site_url,
        'sameAs' => [
            'https://www.facebook.com/goldenticketrealty',
            'https://www.linkedin.com/company/goldenticketrealty',
            'https://www.instagram.com/goldenticketrealty'
        ]
    ];

    echo "<script type=\"application/ld+json\">" . json_encode($local_business, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . "</script>\n";
    echo "<script type=\"application/ld+json\">" . json_encode($faq_page, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . "</script>\n";
    echo "<script type=\"application/ld+json\">" . json_encode($organization, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . "</script>\n";
}, 2);
